from typing import TypeVar

T = TypeVar('T')


class EmptyBuffer:
    def __new__(self, t: T, length: int) -> None:
        return (t*length)()
