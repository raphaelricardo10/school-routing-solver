import ctypes
from domain.vehicle import Vehicle
from abi.structures.model_list import ModelList


class C_Vehicle(ctypes.Structure):
    _fields_ = [
        ("usage", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("capacity", ctypes.c_uint32),
    ]

    @staticmethod
    def from_obj(vehicle: Vehicle):
        return C_Vehicle(vehicle.usage, vehicle.id, vehicle.capacity)

    def to_obj(self):
        return Vehicle(self.id, self.capacity, self.usage)


class C_VehicleList(ModelList):
    @staticmethod
    def from_obj(vehicles: 'list[Vehicle]') -> 'list[C_Vehicle]':
        return ModelList.from_obj(vehicles, C_Vehicle)

    def to_obj(self) -> 'list[Vehicle]':
        return super().to_obj()
