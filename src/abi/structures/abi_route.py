import ctypes

from abi.structures.empty_buffer import EmptyBuffer


class ABIRoute(ctypes.Structure):
    _fields_ = [
        ("vehicle_id", ctypes.c_uint32),
        ("stop_ids", ctypes.POINTER(ctypes.c_uint32)),
        ("number_of_stops", ctypes.c_size_t),
        ("total_distance", ctypes.c_float),
    ]

    def __init__(self, number_of_stops: int, *args, **kw) -> None:
        stop_ids = EmptyBuffer(ctypes.c_uint32, number_of_stops)
        super().__init__(stop_ids=stop_ids, *args, **kw)
