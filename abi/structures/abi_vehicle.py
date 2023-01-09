import ctypes
from domain.vehicle import Vehicle
from abi.structures.model_list import ModelList


class ABIVehicle(ctypes.Structure):
    _fields_ = [
        ("usage", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("capacity", ctypes.c_uint32),
    ]

    @staticmethod
    def from_obj(vehicle: Vehicle):
        return ABIVehicle(vehicle.usage, vehicle.id, vehicle.capacity)

    def to_obj(self):
        return Vehicle(self.id, self.capacity, self.usage)


class ABIVehicleList(ModelList):
    @staticmethod
    def from_obj(vehicles: 'list[Vehicle]') -> 'list[ABIVehicle]':
        return ModelList.from_obj(vehicles, ABIVehicle)

    def to_obj(self) -> 'list[Vehicle]':
        return super().to_obj()
