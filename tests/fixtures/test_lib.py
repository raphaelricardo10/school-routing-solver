import os
from dotenv import load_dotenv

import ctypes
import numpy as np

from pytest import fixture

from abi.abi_function import C_Function
from abi.shared_library import SharedLibrary
from abi.structures.empty_buffer import EmptyBuffer

from domain.stop import Stop
from domain.vehicle import Vehicle

from abi.structures.abi_stop import C_Stop
from abi.structures.abi_vehicle import C_Vehicle, C_VehicleList
from abi.structures.abi_distance_matrix import C_DistanceMatrix, C_DistanceMatrixEntry


class TestLib(SharedLibrary):
    def __init__(self, path: str):
        functions = [
            C_Function('update_vehicle', [C_Vehicle], C_Vehicle),
            C_Function('update_stop', [C_Stop], C_Stop),
            C_Function('add_vehicle_to_array', [
                       (C_Vehicle * 2)], (C_Vehicle * 3)),
            C_Function('read_distance_matrix', [
                       (C_DistanceMatrixEntry * 4),  # Distances
                       ctypes.c_size_t,  # Number of entries
                       ctypes.c_uint32,  # Point A
                       ctypes.c_uint32,  # Point B
                       ], ctypes.c_double),  # Return (distance)
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
        result = EmptyBuffer(C_Vehicle, 3)

        self._run('add_vehicle_to_array', C_VehicleList.from_obj(vehicles),
                  number_of_vehicles, result)

        return C_VehicleList(result).to_obj()

    def read_distance_matrix(self, distances: 'list[list[float]]', a: int, b: int) -> float:
        return self._run('read_distance_matrix', C_DistanceMatrix.from_obj(distances), len(distances), a, b)


@fixture
def test_lib() -> TestLib:
    load_dotenv()
    try:
        lib_path = os.environ['LIB_PATH']
        return TestLib(lib_path)

    except KeyError:
        raise ValueError('Please, provide the LIB_PATH variable in .env file')
