import ctypes
from typing import Type, TypeVar
from collections import UserList
from dataclasses import dataclass

T = TypeVar('T', bound=ctypes.Structure)
U = TypeVar('U')

class ModelList(UserList):
    @staticmethod
    def from_obj(models: 'list[U]', C_Model: Type[T]) -> T:
        c_models = [C_Model.from_obj(x) for x in models]

        return (C_Model * len(models))(*c_models)

    def to_obj(self) -> 'list[U]':
        return [x.to_obj() for x in self]