from __future__ import annotations

import ctypes
import numpy as np

from routingGA import RoutingGA

from abi.abi_function import ABIFunction
from abi.shared_library import SharedLibrary


class GALib(SharedLibrary):
    def __init__(self, routingGA: RoutingGA, libPath: str) -> GALib:
        self.routingGA = routingGA

        numRows, numCols = routingGA.distances.shape

        super().__init__(
            libPath,
            functions=[
                ABIFunction(
                    name="ga_interface",
                    arg_types=[
                        ctypes.c_int,  # Population size
                        ctypes.c_int,  # Quantity of locations
                        ctypes.c_int,  # Quantity of routes
                        ctypes.c_int,  # Maximum of generations
                        ctypes.c_int,  # Selection K value
                        ctypes.c_float,  # Mutation rate
                        ctypes.c_float,  # 2-opt rate
                        np.ctypeslib.ndpointer(  # Distance matrix
                            dtype=np.int32, ndim=2, shape=(numRows, numCols)
                        ),
                        np.ctypeslib.ndpointer(  # Output vector
                            dtype=np.int32,
                            shape=(routingGA.qtyLocations + routingGA.qtyRoutes,),
                        ),
                    ],
                )
            ],
        )

    def run(self):
        result = np.zeros(
            shape=(self.routingGA.qtyLocations + self.routingGA.qtyRoutes),
            dtype=np.int32,
        )

        self.lib.ga_interface(
            self.routingGA.popSize,
            self.routingGA.qtyLocations,
            self.routingGA.qtyRoutes,
            self.routingGA.maxGenerations,
            self.routingGA.selectionK,
            self.routingGA.mutationRate,
            self.routingGA.optRate,
            self.routingGA.distances,
            result,
        )

        return self.routingGA.split_routes(result.tolist())
