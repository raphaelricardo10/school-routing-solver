import os
from dotenv import load_dotenv

import ctypes
import numpy as np

from pytest import fixture

from c_interface.c_function import C_Function
from c_interface.shared_library import SharedLibrary

from domain.stop import Stop
from domain.vehicle import Vehicle

from c_interface.c_structures.c_stop import C_Stop
from c_interface.c_structures.c_vehicle import C_Vehicle
from c_interface.c_structures.c_distance_matrix import C_DistanceMatrix


class TestLib(SharedLibrary):
    def __init__(self, path: str):
        functions = [
            C_Function('update_vehicle', [C_Vehicle], C_Vehicle),
            C_Function('update_stop', [C_Stop], C_Stop),
            C_Function('add_vehicle_to_array', [
                       (C_Vehicle * 2)], (C_Vehicle * 3)),
            C_Function('read_distance_matrix', [
                       np.ctypeslib.ndpointer(
                           dtype=np.float64, ndim=2, shape=(2, 2)),
                       ctypes.c_size_t,
                       ctypes.c_size_t,
                       ctypes.c_size_t
                       ], ctypes.c_double),
        ]

        super().__init__(path, functions)

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        result: C_Vehicle = self._run(
            'update_vehicle', C_Vehicle.from_obj(vehicle))

        return result.to_obj()

    def update_stop(self, stop: Stop) -> Stop:
        result: C_Stop = self._run('update_stop', C_Stop.from_obj(stop))

        return result.to_obj()

    def add_vehicle(self, vehicles: 'list[Vehicle]', number_of_vehicles: int) -> 'list[Vehicle]':
        c_vehicles = [C_Vehicle.from_obj(x) for x in vehicles]
        c_vehicles = (C_Vehicle * 2)(*c_vehicles)
        result = (C_Vehicle * 3)()

        self._run('add_vehicle_to_array', c_vehicles,
                  number_of_vehicles, result)

        return [x.to_obj() for x in result]

    def read_distance_matrix(self, distances: 'list[list[float]]', a: int, b: int) -> float:
        return self._run('read_distance_matrix', C_DistanceMatrix.from_obj(distances), 2, a, b)


@fixture
def test_lib() -> TestLib:
    load_dotenv()
    try:
        lib_path = os.environ['LIB_PATH']
        return TestLib(lib_path)

    except KeyError:
        raise ValueError('Please, provide the LIB_PATH variable in .env file')
