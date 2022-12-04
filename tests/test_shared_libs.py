from domain.stop import Stop
from domain.vehicle import Vehicle

from tests.fixtures.test_lib import test_lib, TestLib


def test_can_update_vehicle_with_library(test_lib: TestLib):
    vehicle = Vehicle(0, 100)

    result = test_lib.update_vehicle(vehicle)

    assert result.id == 2
    assert result.usage == 10
    assert result.capacity == 100

def test_can_update_stop_with_library(test_lib: TestLib):
    stop = Stop(0, 1)

    result = test_lib.update_stop(stop)

    assert result.id == 2
    assert result.usage == 10

def test_can_add_vehicle_to_array_from_library(test_lib: TestLib):
    vehicles = [Vehicle(0, 100, 0), Vehicle(1, 50, 0)]
    
    result = test_lib.add_vehicle(vehicles, 2)

    assert len(result) == 3
    
    assert result[2].id == 3
    assert result[2].capacity == 130
    assert result[2].usage == 0
    
    
def test_can_read_distance_matrix_from_library(test_lib: TestLib):
    distances = [[0,1], [2, 3]]

    for i, row in enumerate(distances):
        for j, distance in enumerate(row):
            assert test_lib.read_distance_matrix(distances, i, j) == distance