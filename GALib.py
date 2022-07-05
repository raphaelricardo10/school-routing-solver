from __future__ import annotations

import numpy as np 
import ctypes

from routingGA import RoutingGA

class GALib:
    def __init__(self, routingGA: RoutingGA, libPath: str) -> GALib:
        self.lib = ctypes.cdll.LoadLibrary('/home/raphael/projects/uff/intcomp/gen-alg-vrp/ga.so')
        self.routingGA = routingGA

        numRows, numCols = routingGA.distances.shape
        self.lib.ga_interface.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, np.ctypeslib.ndpointer(dtype=np.int32, ndim=2, shape=(numRows, numCols))]

    def run(self):
        self.lib.ga_interface(
            self.routingGA.popSize,
            self.routingGA.qtyLocations,
            self.routingGA.qtyRoutes,
            self.routingGA.maxGenerations,
            self.routingGA.selectionK,
            self.routingGA.mutationRate,
            self.routingGA.distances
        )