import numpy as np

class RoutingGA:
    def split_routes(self, genes):
        breakpoints = [0] + genes[self.qtyLocations: ] + [self.qtyLocations]
        routes = []

        for i in range(0, len(breakpoints) - 1):
            route = [0] + genes[breakpoints[i]: breakpoints[i+1]]
            routes.append(route)

        return routes

    def __init__(self, popSize: int = None, qtyLocations: int = None, qtyRoutes: int = None, maxGenerations: int = None, selectionK: int = None, mutationRate: float = None, optRate: float = None, distances: 'list[list[int]]' = None) -> None:
        self.popSize = popSize
        self.qtyLocations = qtyLocations
        self.qtyRoutes = qtyRoutes
        self.maxGenerations = maxGenerations
        self.selectionK = selectionK
        self.mutationRate = mutationRate
        self.optRate = optRate
        self.distances = np.array(distances, dtype=np.int32)