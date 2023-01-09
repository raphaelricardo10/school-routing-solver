import ctypes

from domain.stop import Stop
from abi.structures.model_list import ModelList


class C_Stop(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("usage", ctypes.c_uint32),
    ]

    def from_obj(stop: Stop):
        return C_Stop(stop.id, stop.usage)

    def to_obj(self):
        return Stop(self.id, self.usage)


class C_StopList(ModelList):
    @staticmethod
    def from_obj(stops: 'list[Stop]') -> 'list[C_Stop]':
        return ModelList.from_obj(stops, C_Stop)

    def to_obj(self) -> 'list[Stop]':
        return super().to_obj()
