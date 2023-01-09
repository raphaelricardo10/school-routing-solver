from __future__ import annotations

import ctypes

from domain.stop import Stop
from domain.vehicle import Vehicle

from abi.structures.abi_stop import C_Stop, C_StopList
from abi.structures.abi_vehicle import C_Vehicle, C_VehicleList
from abi.structures.empty_buffer import EmptyBuffer
from abi.structures.abi_distance_matrix import C_DistanceMatrix, C_DistanceMatrixEntry

from abi.shared_library import SharedLibrary


class GAParameters(ctypes.Structure):
    _fields_ = [
        ("population_size", ctypes.c_uint32),
        ("elite_size", ctypes.c_size_t),
        ("mutation_rate", ctypes.c_double),
        ("max_crossover_tries", ctypes.c_int8),
        ("max_generations", ctypes.c_uint32),
    ]

class ArgSizes(ctypes.Structure):
    _fields_ = [
        ("vehicles", ctypes.c_size_t),
        ("stops", ctypes.c_size_t),
        ("distances", ctypes.c_size_t),
        ("result", ctypes.c_size_t),
    ]


class RustSolverLib(SharedLibrary):
    def __init__(self, path: str):
        functions = []

        super().__init__(path, functions)

    def run_genetic_solver(self, vehicles: 'list[Vehicle]', stops: 'list[Stop]', distances: 'list[list[float]]', parameters: GAParameters) -> 'list[int]':
        result_size = len(stops) + len(vehicles)

        arg_types = [
            (C_Vehicle * len(vehicles)),  # Vehicles array pointer
            (C_Stop * len(stops)),  # Stops array pointer
            (C_DistanceMatrixEntry * len(distances)),  # Distance matrix
            ArgSizes, # Length of all pointer arguments
            GAParameters,  # Parameters of genetic algorithm
            (ctypes.c_uint32 * result_size)  # Output vector
        ]

        self._update_arg_types('genetic_solver', arg_types)

        result = EmptyBuffer(ctypes.c_uint32, result_size)

        arg_sizes = ArgSizes(len(vehicles), len(stops), len(distances), result_size)

        self._run('genetic_solver', C_VehicleList.from_obj(vehicles), C_StopList.from_obj(
            stops), C_DistanceMatrix.from_obj(distances), arg_sizes, parameters, result)

        return result
