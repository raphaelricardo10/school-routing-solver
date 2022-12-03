import ctypes

from domain.stop import Stop


class C_Stop(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("usage", ctypes.c_uint32),
    ]

    def to_obj(self):
        return Stop(self.id, self.usage)
