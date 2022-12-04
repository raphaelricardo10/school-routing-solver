import os
from dotenv import load_dotenv

import ctypes

from pytest import fixture

from c_interface.c_function import C_Function
from c_interface.shared_library import SharedLibrary

from domain.stop import Stop
from domain.vehicle import Vehicle

from c_interface.c_structures.c_stop import C_Stop
from c_interface.c_structures.c_vehicle import C_Vehicle


class TestLib(SharedLibrary):
    def __init__(self, path: str):
        functions = [
            C_Function('update_vehicle', [C_Vehicle], C_Vehicle),
            C_Function('update_stop', [C_Stop], C_Stop),
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
        input_array = (C_Vehicle * len(vehicles))
        output_array = (C_Vehicle * (len(vehicles) + 1))

        self._update_arg_types('add_vehicle_to_array', [input_array])
        self._update_return_type('add_vehicle_to_array', output_array)

        c_vehicles = [C_Vehicle.from_obj(x) for x in vehicles]
        c_vehicles = input_array(*c_vehicles)
        result = output_array()

        self._run('add_vehicle_to_array', c_vehicles,
                                           number_of_vehicles, result)

        return [x.to_obj() for x in result]


@fixture
def test_lib() -> TestLib:
    load_dotenv()
    try:
        lib_path = os.environ['LIB_PATH']
        return TestLib(lib_path)

    except KeyError:
        raise ValueError('Please, provide the LIB_PATH variable in .env file')
