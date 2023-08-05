import os
import sys
import logging
import traceback

from warnings import warn

from celery import group, signals, states
from celery.app import trace
from celery.utils.saferepr import saferepr
from celery.concurrency import base
from celery._state import _task_stack
from celery.exceptions import Ignore, InvalidTaskError, Reject, Retry

from billiard.einfo import ExceptionInfo

from kombu.exceptions import EncodeError

logger = logging.getLogger(__name__)


STARTED = states.STARTED
SUCCESS = states.SUCCESS
IGNORED = states.IGNORED
REJECTED = states.REJECTED
RETRY = states.RETRY
FAILURE = states.FAILURE
EXCEPTION_STATES = states.EXCEPTION_STATES
IGNORE_STATES = frozenset({IGNORED, RETRY, REJECTED})

prerun_receivers = signals.task_prerun.receivers
postrun_receivers = signals.task_postrun.receivers
success_receivers = signals.task_success.receivers

send_prerun = signals.task_prerun.send
send_postrun = signals.task_postrun.send
send_success = signals.task_success.send

push_task = _task_stack.push
pop_task = _task_stack.pop


def info(fmt, context):
    """Log 'fmt % context' with severity 'INFO'.

    'context' is also passed in extra with key 'data' for custom handlers.
    """
    logger.info(fmt, context, extra={'data': context})


def report_internal_error(task, exc):
    _type, _value, _tb = sys.exc_info()
    try:
        _value = task.backend.prepare_exception(exc, 'pickle')
        exc_info = ExceptionInfo((_type, _value, _tb), internal=True)
        warn(RuntimeWarning(
            'Exception raised outside body: {0!r}:\n{1}'.format(
                exc, exc_info.traceback)))
        return exc_info
    finally:
        del _tb


def build_async_tracer(
    name,
    task,
    loader=None,
    hostname=None,
    store_errors=True,
    Info=trace.TraceInfo,
    eager=False,
    propagate=False,
    app=None,
    monotonic=base.monotonic,
    trace_ok_t=trace.trace_ok_t,
    IGNORE_STATES=trace.IGNORE_STATES,
):
    """Return a function that traces task execution.

    Catches all exceptions and updates result backend with the
    state and result.

    If the call was successful, it saves the result to the task result
    backend, and sets the task status to `"SUCCESS"`.

    If the call raises :exc:`~@Retry`, it extracts
    the original exception, uses that as the result and sets the task state
    to `"RETRY"`.

    If the call results in an exception, it saves the exception as the task
    result, and sets the task state to `"FAILURE"`.

    Return a function that takes the following arguments:

        :param uuid: The id of the task.
        :param args: List of positional args to pass on to the function.
        :param kwargs: Keyword arguments mapping to pass on to the function.
        :keyword request: Request dict.

    """
    # noqa: C901
    # pylint: disable=too-many-statements

    # If the task doesn't define a custom __call__ method
    # we optimize it away by simply calling the run method directly,
    # saving the extra method call and a line less in the stack trace.
    fun = task if trace.task_has_custom(task, '__call__') else task.run

    loader = loader or app.loader
    backend = task.backend
    ignore_result = task.ignore_result
    track_started = task.track_started
    track_started = not eager and (task.track_started and not ignore_result)
    publish_result = not eager and not ignore_result
    hostname = hostname or trace.gethostname()
    inherit_parent_priority = app.conf.task_inherit_parent_priority

    loader_task_init = loader.on_task_init
    loader_cleanup = loader.on_process_cleanup

    task_on_success = None
    task_after_return = None
    if trace.task_has_custom(task, 'on_success'):
        task_on_success = task.on_success
    if trace.task_has_custom(task, 'after_return'):
        task_after_return = task.after_return

    store_result = backend.store_result
    mark_as_done = backend.mark_as_done
    backend_cleanup = backend.process_cleanup

    pid = os.getpid()

    request_stack = task.request_stack
    push_request = request_stack.push
    pop_request = request_stack.pop
    push_task = _task_stack.push
    pop_task = _task_stack.pop
    _does_info = logger.isEnabledFor(logging.INFO)
    resultrepr_maxsize = task.resultrepr_maxsize

    prerun_receivers = signals.task_prerun.receivers
    postrun_receivers = signals.task_postrun.receivers
    success_receivers = signals.task_success.receivers

    from celery import canvas
    signature = canvas.maybe_signature  # maybe_ does not clone if already

    def on_error(request, exc, uuid, state=FAILURE, call_errbacks=True):
        if propagate:
            raise
        I = Info(state, exc)
        R = I.handle_error_state(
            task, request, eager=eager, call_errbacks=call_errbacks,
        )
        return I, R, I.state, I.retval

    async def trace_task(uuid, args, kwargs, request=None):
        # R      - is the possibly prepared return value.
        # I      - is the Info object.
        # T      - runtime
        # Rstr   - textual representation of return value
        # retval - is the always unmodified return value.
        # state  - is the resulting task state.

        # This function is very long because we've unrolled all the calls
        # for performance reasons, and because the function is so long
        # we want the main variables (I, and R) to stand out visually from the
        # the rest of the variables, so breaking PEP8 is worth it ;)
        R = I = T = Rstr = retval = state = None
        task_request = None
        time_start = monotonic()
        try:
            try:
                kwargs.items
            except AttributeError:
                raise InvalidTaskError(
                    'Task keyword arguments is not a mapping')
            push_task(task)
            task_request = trace.Context(
                request or {},
                args=args,
                called_directly=False,
                kwargs=kwargs,
            )
            root_id = task_request.root_id or uuid
            task_priority = task_request.delivery_info.get('priority') if \
                inherit_parent_priority else None
            push_request(task_request)
            try:
                # -*- PRE -*-
                if prerun_receivers:
                    send_prerun(sender=task, task_id=uuid, task=task,
                                args=args, kwargs=kwargs)
                loader_task_init(uuid, task)
                if track_started:
                    store_result(
                        uuid, {'pid': pid, 'hostname': hostname}, STARTED,
                        request=task_request,
                    )

                # -*- TRACE -*-
                try:
                    R = retval = await fun(*args, **kwargs)
                    state = SUCCESS
                except Reject as exc:
                    I, R = Info(REJECTED, exc), ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_reject(task, task_request)
                except Ignore as exc:
                    I, R = Info(IGNORED, exc), ExceptionInfo(internal=True)
                    state, retval = I.state, I.retval
                    I.handle_ignore(task, task_request)
                except Retry as exc:
                    I, R, state, retval = on_error(
                        task_request, exc, uuid, RETRY, call_errbacks=False)
                except Exception as exc:
                    traceback.print_exc()
                    I, R, state, retval = on_error(task_request, exc, uuid)
                except BaseException:
                    traceback.print_exc()
                    raise
                else:
                    try:
                        # callback tasks must be applied before the result is
                        # stored, so that result.children is populated.

                        # groups are called inline and will store trail
                        # separately, so need to call them separately
                        # so that the trail's not added multiple times :(
                        # (Issue #1936)
                        callbacks = task.request.callbacks
                        if callbacks:
                            if len(task.request.callbacks) > 1:
                                sigs, groups = [], []
                                for sig in callbacks:
                                    sig = signature(sig, app=app)
                                    if isinstance(sig, group):
                                        groups.append(sig)
                                    else:
                                        sigs.append(sig)
                                for group_ in groups:
                                    group_.apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                                if sigs:
                                    group(sigs, app=app).apply_async(
                                        (retval,),
                                        parent_id=uuid, root_id=root_id,
                                        priority=task_priority
                                    )
                            else:
                                signature(callbacks[0], app=app).apply_async(
                                    (retval,), parent_id=uuid, root_id=root_id,
                                    priority=task_priority
                                )

                        # execute first task in chain
                        chain = task_request.chain
                        if chain:
                            _chsig = signature(chain.pop(), app=app)
                            _chsig.apply_async(
                                (retval,), chain=chain,
                                parent_id=uuid, root_id=root_id,
                                priority=task_priority
                            )
                        mark_as_done(
                            uuid, retval, task_request, publish_result,
                        )
                    except EncodeError as exc:
                        I, R, state, retval = on_error(task_request, exc, uuid)
                    else:
                        Rstr = saferepr(R, resultrepr_maxsize)
                        T = monotonic() - time_start
                        if task_on_success:
                            task_on_success(retval, uuid, args, kwargs)
                        if success_receivers:
                            send_success(sender=task, result=retval)
                        if _does_info:
                            task_name = trace.get_task_name(task_request, name)
                            info(trace.LOG_SUCCESS, {
                                'id': uuid,
                                'name': task_name,
                                'return_value': Rstr,
                                'runtime': T,
                            })

                # -* POST *-
                if state not in trace.IGNORE_STATES:
                    if task_after_return:
                        task_after_return(
                            state, retval, uuid, args, kwargs, None,
                        )
            finally:
                try:
                    if postrun_receivers:
                        send_postrun(sender=task, task_id=uuid, task=task,
                                     args=args, kwargs=kwargs,
                                     retval=retval, state=state)
                finally:
                    pop_task()
                    pop_request()
                    if not eager:
                        try:
                            backend_cleanup()
                            loader_cleanup()
                        except (KeyboardInterrupt, SystemExit, MemoryError):
                            raise
                        except Exception as exc:
                            traceback.print_exc()
                            logger.error('Process cleanup failed: %r', exc,
                                         exc_info=True)
        except MemoryError:
            raise
        except Exception as exc:
            traceback.print_exc()
            if eager:
                raise
            R = report_internal_error(task, exc)
            if task_request is not None:
                I, _, _, _ = on_error(task_request, exc, uuid)
        return trace_ok_t(R, I, T, Rstr)

    return trace_task
