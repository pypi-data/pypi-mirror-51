########################################################################
# File name: utils.py
# This file is part of: aioxmpp
#
# LICENSE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
########################################################################
import asyncio
import contextlib
import types

import lxml.etree as etree

__all__ = [
    "etree",
    "namespaces",
]

namespaces = types.SimpleNamespace()
namespaces.xmlstream = "http://etherx.jabber.org/streams"
namespaces.client = "jabber:client"
namespaces.starttls = "urn:ietf:params:xml:ns:xmpp-tls"
namespaces.sasl = "urn:ietf:params:xml:ns:xmpp-sasl"
namespaces.stanzas = "urn:ietf:params:xml:ns:xmpp-stanzas"
namespaces.streams = "urn:ietf:params:xml:ns:xmpp-streams"
namespaces.stream_management = "urn:xmpp:sm:3"
namespaces.bind = "urn:ietf:params:xml:ns:xmpp-bind"
namespaces.aioxmpp = "https://zombofant.net/xmlns/aioxmpp"
namespaces.aioxmpp_test = "https://zombofant.net/xmlns/aioxmpp#test"
namespaces.aioxmpp_internal = "https://zombofant.net/xmlns/aioxmpp#internal"
namespaces.xml = "http://www.w3.org/XML/1998/namespace"


@contextlib.contextmanager
def background_task(coro, logger):
    def log_result(task):
        try:
            result = task.result()
        except asyncio.CancelledError:
            logger.debug("background task terminated by CM exit: %r",
                         task)
        except:  # NOQA
            logger.error("background task failed: %r",
                         task,
                         exc_info=True)
        else:
            if result is not None:
                logger.info("background task (%r) returned a value: %r",
                            task,
                            result)

    task = asyncio.ensure_future(coro)
    task.add_done_callback(log_result)
    try:
        yield
    finally:
        task.cancel()


class magicmethod:
    __slots__ = ("_f",)

    def __init__(self, f):
        super().__init__()
        self._f = f

    def __get__(self, instance, class_):
        if instance is None:
            return types.MethodType(self._f, class_)
        return types.MethodType(self._f, instance)


def mkdir_exist_ok(path):
    """
    Create a directory (including parents) if it does not exist yet.

    :param path: Path to the directory to create.
    :type path: :class:`pathlib.Path`

    Uses :meth:`pathlib.Path.mkdir`; if the call fails with
    :class:`FileNotFoundError` and `path` refers to a directory, it is treated
    as success.
    """

    try:
        path.mkdir(parents=True)
    except FileExistsError:
        if not path.is_dir():
            raise


class LazyTask(asyncio.Future):
    """
    :class:`asyncio.Future` subclass which spawns a coroutine when it is first
    awaited.

    :param coroutine_function: The coroutine function to invoke.
    :param args: Arguments to pass to `coroutine_function`.

    :class:`LazyTask` objects are awaitable. When the first attempt to await
    them is made, the `coroutine_function` is started with the given `args` and
    the result is awaited. Any further awaits on the :class:`LazyTask` will
    await the same coroutine.
    """

    def __init__(self, coroutine_function, *args):
        super().__init__()
        self.__coroutine_function = coroutine_function
        self.__args = args
        self.__task = None

    def add_done_callback(self, cb, *args):
        self.__start_task()
        return super().add_done_callback(cb, *args)

    def __start_task(self):
        if self.__task is None:
            self.__task = asyncio.ensure_future(
                self.__coroutine_function(*self.__args)
            )
            self.__task.add_done_callback(self.__task_done)

    def __task_done(self, task):
        if task.exception():
            self.set_exception(task.exception())
        else:
            self.set_result(task.result())

    def __iter__(self):
        self.__start_task()
        return iter(self.__task)

    if hasattr(asyncio.Future, "__await__"):
        def __await__(self):
            self.__start_task()
            return super().__await__()


@asyncio.coroutine
def gather_reraise_multi(*fut_or_coros, message="gather_reraise_multi"):
    """
    Wrap all the arguments `fut_or_coros` in futures with
    :func:`asyncio.ensure_future` and wait until all of them are finish or
    fail.

    :param fut_or_coros: the futures or coroutines to wait for
    :type fut_or_coros: future or coroutine
    :param message: the message included with the raised
        :class:`aioxmpp.errrors.GatherError` in the case of failure.
    :type message: :class:`str`
    :returns: the list of the results of the arguments.
    :raises aioxmpp.errors.GatherError: if any of the futures or
        coroutines fail.

    If an exception was raised, reraise all exceptions wrapped in a
    :class:`aioxmpp.errors.GatherError` with the message set to
    `message`.

    .. note::

       This is similar to the standard function
       :func:`asyncio.gather`, but avoids the in-band signalling of
       raised exceptions as return values, by raising exceptions bundled
       as a :class:`aioxmpp.errors.GatherError`.

    .. note::

       Use this function only if you are either

       a) not interested in the return values, or

       b) only interested in the return values if all futures are
          successful.
    """
    # this late import is needed for Python 3.4
    from aioxmpp import errors

    todo = [asyncio.ensure_future(fut_or_coro) for fut_or_coro in fut_or_coros]
    if not todo:
        return []

    yield from asyncio.wait(todo)
    results = []
    exceptions = []
    for fut in todo:
        if fut.exception() is not None:
            exceptions.append(fut.exception())
        else:
            results.append(fut.result())
    if exceptions:
        raise errors.GatherError(message, exceptions)
    return results
