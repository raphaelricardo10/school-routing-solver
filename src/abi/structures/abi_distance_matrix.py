from __future__ import annotations

import ctypes
from abi.structures.model_list import ModelList


class ABIDistanceMatrixEntry(ctypes.Structure):
    _fields_ = [
        ("from", ctypes.c_int32),
        ("to", ctypes.c_int32),
        ("distance", ctypes.c_double),
    ]

    @staticmethod
    def from_obj(entry: list) -> ABIDistanceMatrixEntry:
        return ABIDistanceMatrixEntry(*entry[:3])

    def to_obj(self) -> list:
        return [getattr(self, "from"), self.to, self.distance]


class ABIDistanceMatrix(ModelList):
    @staticmethod
    def from_obj(distances: "list[list[float]]") -> "list[ABIDistanceMatrixEntry]":
        return ModelList.from_obj(distances, ABIDistanceMatrixEntry)

    def to_obj(self) -> "list[list[float]]":
        return super().to_obj()
