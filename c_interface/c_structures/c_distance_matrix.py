import numpy as np

from c_interface.c_structures.c_structure import C_Structure


class C_DistanceMatrix(C_Structure):
    
    def from_obj(distances: 'list[list[float]]') -> 'np.ndarray[np.float64, np.float64]':
        return np.array(distances, dtype=np.float64)

    def to_obj(distances: 'np.ndarray[float]') -> 'list[list[float]]':
        return distances.tolist()