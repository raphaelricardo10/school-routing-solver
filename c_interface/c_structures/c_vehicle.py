import ctypes

from domain.vehicle import Vehicle


class c_size_tC_Vehicle(ctypes.Structure):
    _fields_ = [
        ("usage", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("capacity", ctypes.c_uint32),
    ]

    def to_obj(self):
        return Vehicle(self.id, self.capacity, self.usage)
