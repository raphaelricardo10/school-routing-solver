import ctypes
from typing import TypeVar

T = TypeVar("T", bound=ctypes.Structure)


class EmptyBuffer:
    def __new__(cls, t: T, length: int, *args, **kwargs) -> None:
        if args or kwargs:
            objs = [t(*args, **kwargs) for _ in range(length)]
            return (t * length)(*objs)

        return (t * length)()
