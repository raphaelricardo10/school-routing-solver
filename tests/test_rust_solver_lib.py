from domain.stop import Stop
from domain.vehicle import Vehicle

from c_interface.libs.rust_solver_lib import GAParameters, RustSolverLib

from tests.fixtures.rust_solver_lib import rust_solver_lib
from tests.fixtures.domain import vehicles, stops, distances
from tests.fixtures.genetic_algorithm import genetic_algorithm_parameters


def test_can_get_solution_from_genetic_algorithm(vehicles: 'list[Vehicle]', stops: 'list[Stop]', distances: 'list[list]', genetic_algorithm_parameters: GAParameters, rust_solver_lib: RustSolverLib):
    result = rust_solver_lib.run_genetic_solver(vehicles, stops, distances, genetic_algorithm_parameters)

    print(result)
