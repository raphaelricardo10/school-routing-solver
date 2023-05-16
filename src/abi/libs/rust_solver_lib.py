from __future__ import annotations

import ctypes
from enum import Enum

from domain.stop import Stop
from domain.route import Route
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
        ("mutation_rate", ctypes.c_float),
        ("local_search_rate", ctypes.c_float),
        ("max_crossover_tries", ctypes.c_int8),
        ("max_generations", ctypes.c_uint32),
    ]


class GraspParameters(ctypes.Structure):
    _fields_ = [
        ("rcl_size", ctypes.c_size_t),
        ("max_improvement_times", ctypes.c_uint8),
    ]


class ArgSizes(ctypes.Structure):
    _fields_ = [
        ("vehicles", ctypes.c_size_t),
        ("stops", ctypes.c_size_t),
        ("distances", ctypes.c_size_t),
        ("result", ctypes.c_size_t),
    ]


class RustSolverLibFunctions(Enum):
    GRASP_GENETIC = "grasp_genetic_solver"


class RustSolverLib(SharedLibrary):
    def __init__(self, path: str):
        functions = [
            ABIFunction(
                name=RustSolverLibFunctions.GRASP_GENETIC.value,
                arg_types=[
                    (ctypes.POINTER(ABIVehicle)),  # Vehicles array pointer
                    (ctypes.POINTER(ABIStop)),  # Stops array pointer
                    (ctypes.POINTER(ABIDistanceMatrixEntry)),  # Distance matrix
                    ArgSizes,  # Length of all pointer arguments
                    GraspParameters,  # Parameters of GRASP solver
                    GAParameters,  # Parameters of genetic algorithm
                    (ctypes.POINTER(ABIRoute)),  # Output vector
                ],
                return_type=ctypes.POINTER(ABIRoute),
            )
        ]

        super().__init__(path, functions)

    def run_grasp_genetic_solver(
        self,
        vehicles: "list[Vehicle]",
        stops: "list[Stop]",
        distances: "list[list[float]]",
        grasp_parameters: GraspParameters,
        ga_parameters: GAParameters,
    ) -> "list[Route]":
        result: list[ABIRoute] = EmptyBuffer(
            ABIRoute, len(vehicles), number_of_stops=len(stops)
        )

        arg_sizes = ArgSizes(len(vehicles), len(stops), len(distances), len(vehicles))

        self._run(
            RustSolverLibFunctions.GRASP_GENETIC.value,
            ABIVehicleList.from_obj(vehicles),
            ABIStopList.from_obj(stops),
            ABIDistanceMatrix.from_obj(distances),
            arg_sizes,
            grasp_parameters,
            ga_parameters,
            result,
        )

        stops_map = {x.id: x for x in stops}
        result_map = {x.vehicle_id: x for x in result}

        routes = []

        for vehicle in vehicles:
            result_entry = result_map[vehicle.id]

            route_stops = [
                stops_map[x]
                for x in result_entry.stop_ids[: result_entry.number_of_stops]
            ]

            vehicle.usage = sum(x.usage for x in route_stops)

            routes.append(Route(vehicle, route_stops, result_entry.total_distance))

        return routes
