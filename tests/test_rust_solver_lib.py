from domain.stop import Stop
from domain.vehicle import Vehicle

from abi.libs.rust_solver_lib import GAParameters, RustSolverLib


def test_can_get_solution_from_genetic_algorithm(
    vehicles: "list[Vehicle]",
    stops: "list[Stop]",
    distances: "list[list]",
    genetic_algorithm_parameters: GAParameters,
    rust_solver_lib: RustSolverLib,
):
    rust_solver_lib.run_genetic_solver(
        vehicles, stops, distances, genetic_algorithm_parameters
    )
