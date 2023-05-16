import math
from pytest import fixture

from domain.stop import Stop
from abi.libs.rust_solver_lib import GraspParameters


@fixture
def grasp_algorithm_parameters(stops: list[Stop]):
    return GraspParameters(
        rcl_size=math.floor(0.3 * len(stops)), max_improvement_times=10
    )
