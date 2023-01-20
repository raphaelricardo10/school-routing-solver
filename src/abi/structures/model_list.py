import ctypes
from typing import Type, TypeVar
from collections import UserList
from dataclasses import dataclass

T = TypeVar("T", bound=ctypes.Structure)
U = TypeVar("U")


class ModelList(UserList):
    @staticmethod
    def from_obj(models: "list[U]", abi_model: Type[T]) -> T:
        c_models = [abi_model.from_obj(x) for x in models]

        return (abi_model * len(models))(*c_models)

    def to_obj(self) -> "list[U]":
        return [x.to_obj() for x in self]
