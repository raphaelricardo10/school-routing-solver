import ctypes

from domain.vehicle import Vehicle


class C_Vehicle(ctypes.Structure):
    _fields_ = [
        ("usage", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("capacity", ctypes.c_uint32),
    ]

    def from_obj(vehicle: Vehicle):
        return C_Vehicle(vehicle.usage, vehicle.id, vehicle.capacity)

    def to_obj(self):
        return Vehicle(self.id, self.capacity, self.usage)
