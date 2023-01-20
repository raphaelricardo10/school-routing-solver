from domain.stop import Stop
from domain.vehicle import Vehicle

from dataclasses import dataclass


@dataclass
class Route:
    vehicle: Vehicle
    stops: "list[Stop]"
    total_distance: float
