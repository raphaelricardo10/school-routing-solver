import ctypes

from domain.route import Route
from abi.structures.abi_stop import C_Stop
from abi.structures.abi_vehicle import C_Vehicle
from abi.structures.model_list import ModelList


class C_Route(ctypes.Structure):
    _fields_ = [
        ("vehicle", C_Vehicle),
        ("stops", ctypes.POINTER(C_Stop)),
        ("number_of_stops", ctypes.c_uint32),
        ("total_distance", ctypes.c_double),
    ]

    def from_obj(route: Route):
        return C_Route(route.vehicle, route.stops, len(route.stops), route.total_distance)

    def to_obj(self):
        return Route(self.vehicle, [], self.total_distance)


class C_VehicleList(ModelList):
    @staticmethod
    def from_obj(routes: 'list[Route]') -> 'list[C_Route]':
        return ModelList.from_obj(routes, C_Route)

    def to_obj(self) -> 'list[Route]':
        return super().to_obj()
