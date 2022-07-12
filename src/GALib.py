from __future__ import annotations

import numpy as np 
import ctypes

from routingGA import RoutingGA

class GALib:
    def __init__(self, routingGA: RoutingGA, libPath: str) -> GALib:
        self.lib = ctypes.cdll.LoadLibrary(libPath)
        self.routingGA = routingGA

        numRows, numCols = routingGA.distances.shape
        self.lib.ga_interface.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_float,
            ctypes.c_float,
            np.ctypeslib.ndpointer(dtype=np.int32, ndim=2, shape=(numRows, numCols)),
            np.ctypeslib.ndpointer(dtype=np.int32, shape=(routingGA.qtyLocations + routingGA.qtyRoutes, ))
        ]

    def run(self):
        result = np.zeros(shape=(self.routingGA.qtyLocations + self.routingGA.qtyRoutes), dtype=np.int32)

        self.lib.ga_interface(
            self.routingGA.popSize,
            self.routingGA.qtyLocations,
            self.routingGA.qtyRoutes,
            self.routingGA.maxGenerations,
            self.routingGA.selectionK,
            self.routingGA.mutationRate,
            self.routingGA.optRate,
            self.routingGA.distances,
            result
        )

        return self.routingGA.split_routes(result.tolist())