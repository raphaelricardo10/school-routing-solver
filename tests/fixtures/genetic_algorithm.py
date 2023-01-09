from pytest import fixture

from abi.libs.rust_solver_lib import GAParameters

@fixture
def genetic_algorithm_parameters():
    return GAParameters(
        population_size=10,
        elite_size=3,
        mutation_rate=0.05,
        max_crossover_tries=20,
        max_generations=100,
    )

