from dataclasses import dataclass

@dataclass
class Vehicle:
    id: int
    capacity: int
    usage: int = 0