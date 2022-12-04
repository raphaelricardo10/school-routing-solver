import ctypes

from domain.stop import Stop


class C_Stop(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("usage", ctypes.c_uint32),
    ]

    def from_obj(stop: Stop):
        return C_Stop(stop.id, stop.usage)

    def to_obj(self):
        return Stop(self.id, self.usage)
