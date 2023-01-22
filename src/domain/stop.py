from typing import Optional
from dataclasses import dataclass


@dataclass
class Stop:
    id: int
    usage: int
    address: Optional[int] = None
