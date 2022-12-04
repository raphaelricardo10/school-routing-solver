import ctypes

from domain.route import Route
from c_interface.c_structures.c_stop import C_Stop
from c_interface.c_structures.c_vehicle import C_Vehicle


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
