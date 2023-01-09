import os
from dotenv import load_dotenv

from pytest import fixture

from abi.libs.rust_solver_lib import RustSolverLib


@fixture
def rust_solver_lib() -> RustSolverLib:
    load_dotenv()
    try:
        lib_path = os.environ['LIB_PATH']
        return RustSolverLib(lib_path)

    except KeyError:
        raise ValueError('Please, provide the LIB_PATH variable in .env file')
