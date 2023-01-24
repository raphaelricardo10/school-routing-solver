from __future__ import annotations

import ctypes

from domain.stop import Stop
from domain.vehicle import Vehicle

from abi.abi_function import ABIFunction
from abi.structures.empty_buffer import EmptyBuffer
from abi.structures.abi_route import ABIRoute
from abi.structures.abi_stop import ABIStop, ABIStopList
from abi.structures.abi_vehicle import ABIVehicle, ABIVehicleList
from abi.structures.abi_distance_matrix import ABIDistanceMatrix, ABIDistanceMatrixEntry

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
        functions = [
            ABIFunction(
                name="genetic_solver",
                arg_types=[
                    (ctypes.POINTER(ABIVehicle)),  # Vehicles array pointer
                    (ctypes.POINTER(ABIStop)),  # Stops array pointer
                    (ctypes.POINTER(ABIDistanceMatrixEntry)),  # Distance matrix
                    ArgSizes,  # Length of all pointer arguments
                    GAParameters,  # Parameters of genetic algorithm
                    (ctypes.POINTER(ABIRoute)),  # Output vector
                ],
                return_type=ctypes.POINTER(ABIRoute),
            )
        ]

        super().__init__(path, functions)

    def run_genetic_solver(
        self,
        vehicles: "list[Vehicle]",
        stops: "list[Stop]",
        distances: "list[list[float]]",
        parameters: GAParameters,
    ) -> "list[ABIRoute]":
        result: list[ABIRoute] = EmptyBuffer(ABIRoute, len(vehicles), number_of_stops=len(stops))

        arg_sizes = ArgSizes(len(vehicles), len(stops), len(distances), len(vehicles))

        self._run(
            "genetic_solver",
            ABIVehicleList.from_obj(vehicles),
            ABIStopList.from_obj(stops),
            ABIDistanceMatrix.from_obj(distances),
            arg_sizes,
            parameters,
            result,
        )

        return result
