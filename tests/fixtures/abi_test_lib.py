import os
from dotenv import load_dotenv

import ctypes

from pytest import fixture

from abi.abi_function import ABIFunction
from abi.shared_library import SharedLibrary
from abi.structures.empty_buffer import EmptyBuffer

from domain.stop import Stop
from domain.vehicle import Vehicle

from abi.structures.abi_stop import ABIStop
from abi.structures.abi_vehicle import ABIVehicle, ABIVehicleList
from abi.structures.abi_distance_matrix import ABIDistanceMatrix, ABIDistanceMatrixEntry


class ABITestLib(SharedLibrary):
    def __init__(self, path: str):
        functions = [
            ABIFunction("update_vehicle", [ABIVehicle], ABIVehicle),
            ABIFunction("update_stop", [ABIStop], ABIStop),
            ABIFunction("add_vehicle_to_array", [(ABIVehicle * 2)], (ABIVehicle * 3)),
            ABIFunction(
                "read_distance_matrix",
                [
                    (ABIDistanceMatrixEntry * 4),  # Distances
                    ctypes.c_size_t,  # Number of entries
                    ctypes.c_uint32,  # Point A
                    ctypes.c_uint32,  # Point B
                ],
                ctypes.c_double,
            ),  # Return (distance)
        ]

        super().__init__(path, functions)

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        result: ABIVehicle = self._run("update_vehicle", ABIVehicle.from_obj(vehicle))

        return result.to_obj()

    def update_stop(self, stop: Stop) -> Stop:
        result: ABIStop = self._run("update_stop", ABIStop.from_obj(stop))

        return result.to_obj()

    def add_vehicle(
        self, vehicles: "list[Vehicle]", number_of_vehicles: int
    ) -> "list[Vehicle]":
        result = EmptyBuffer(ABIVehicle, 3)

        self._run(
            "add_vehicle_to_array",
            ABIVehicleList.from_obj(vehicles),
            number_of_vehicles,
            result,
        )

        return ABIVehicleList(result).to_obj()

    def read_distance_matrix(
        self, distances: "list[list[float]]", a: int, b: int
    ) -> float:
        return self._run(
            "read_distance_matrix",
            ABIDistanceMatrix.from_obj(distances),
            len(distances),
            a,
            b,
        )


@fixture
def test_lib() -> ABITestLib:
    load_dotenv()
    try:
        RUST_SOLVER_LIB = os.environ["RUST_SOLVER_LIB"]
        return ABITestLib(RUST_SOLVER_LIB)

    except KeyError:
        raise ValueError("Please, provide the RUST_SOLVER_LIB variable in .env file")
