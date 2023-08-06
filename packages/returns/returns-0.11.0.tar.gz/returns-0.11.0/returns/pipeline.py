# -*- coding: utf-8 -*-

from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, Coroutine, TypeVar, Union, overload

from returns.generated.pipe import _pipe as pipe  # noqa: F401, WPS436
from returns.maybe import Maybe
from returns.primitives.exceptions import UnwrapFailedError
from returns.result import Result

# Logical aliases:
_Unwrapable = Union[Result, Maybe]

# Just aliases:
_FirstType = TypeVar('_FirstType')
_SecondType = TypeVar('_SecondType')

# Hacks for functions:
_ReturnsResultType = TypeVar(
    '_ReturnsResultType',
    bound=Callable[..., _Unwrapable],
)
_AsyncReturnsResultType = TypeVar(
    '_AsyncReturnsResultType',
    bound=Callable[..., Coroutine[_FirstType, _SecondType, _Unwrapable]],
)


def is_successful(container: _Unwrapable) -> bool:
    """
    Determins if a container was successful or not.

    We treat container that raise ``UnwrapFailedError`` on ``.unwrap()``
    not successful.

    .. code:: python

      >>> from returns.maybe import Some, Nothing
      >>> from returns.result import Failure, Success
      >>> is_successful(Some(1))
      True
      >>> is_successful(Nothing)
      False
      >>> is_successful(Success(1))
      True
      >>> is_successful(Failure(1))
      False

    """
    try:
        container.unwrap()
    except UnwrapFailedError:
        return False
    else:
        return True


@overload
def pipeline(
    function: _AsyncReturnsResultType,
) -> _AsyncReturnsResultType:
    """Case for async functions."""


@overload
def pipeline(function: _ReturnsResultType) -> _ReturnsResultType:
    """Case for regular functions."""


def pipeline(function):  # noqa: C901
    """
    Decorator to enable ``do-notation`` context.

    Should be used for series of computations that rely on ``.unwrap`` method.

    Supports both async and regular functions.
    """
    if iscoroutinefunction(function):
        async def decorator(*args, **kwargs):  # noqa: WPS430
            try:
                return await function(*args, **kwargs)
            except UnwrapFailedError as exc:
                return exc.halted_container
    else:
        def decorator(*args, **kwargs):  # noqa: WPS430
            try:
                return function(*args, **kwargs)
            except UnwrapFailedError as exc:
                return exc.halted_container
    return wraps(function)(decorator)
