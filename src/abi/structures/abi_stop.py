import ctypes

from domain.stop import Stop
from abi.structures.model_list import ModelList


class ABIStop(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("usage", ctypes.c_uint32),
    ]

    def from_obj(stop: Stop):
        return ABIStop(stop.id, stop.usage)

    def to_obj(self):
        return Stop(self.id, self.usage)


class ABIStopList(ModelList):
    @staticmethod
    def from_obj(stops: "list[Stop]") -> "list[ABIStop]":
        return ModelList.from_obj(stops, ABIStop)

    def to_obj(self) -> "list[Stop]":
        return super().to_obj()
