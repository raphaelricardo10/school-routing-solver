import ctypes

from domain.route import Route
from abi.structures.abi_stop import ABIStop
from abi.structures.abi_vehicle import ABIVehicle
from abi.structures.model_list import ModelList


class ABIRoute(ctypes.Structure):
    _fields_ = [
        ("vehicle", ABIVehicle),
        ("stops", ctypes.POINTER(ABIStop)),
        ("number_of_stops", ctypes.c_uint32),
        ("total_distance", ctypes.c_double),
    ]

    def from_obj(route: Route):
        return ABIRoute(route.vehicle, route.stops, len(route.stops), route.total_distance)

    def to_obj(self):
        return Route(self.vehicle, [], self.total_distance)


class ABIVehicleList(ModelList):
    @staticmethod
    def from_obj(routes: 'list[Route]') -> 'list[ABIRoute]':
        return ModelList.from_obj(routes, ABIRoute)

    def to_obj(self) -> 'list[Route]':
        return super().to_obj()
