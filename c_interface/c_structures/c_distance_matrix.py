from __future__ import annotations

import ctypes
from c_interface.c_structures.model_list import ModelList


class C_DistanceMatrixEntry(ctypes.Structure):
    _fields_ = [
        ("from", ctypes.c_int32),
        ("to", ctypes.c_int32),
        ("distance", ctypes.c_double)
    ]

    def from_obj(entry: list) -> C_DistanceMatrixEntry:
        return C_DistanceMatrixEntry(*entry[:3])

    def to_obj(self) -> list:
        return [getattr(self, 'from'), self.to, self.distance]


class C_DistanceMatrix(ModelList):

    def from_obj(distances: 'list[list[float]]') -> 'list[C_DistanceMatrixEntry]':
        return ModelList.from_obj(distances, C_DistanceMatrixEntry)

    def to_obj(distances: 'list[C_DistanceMatrixEntry]') -> 'list[list[float]]':
        return super().to_obj()
