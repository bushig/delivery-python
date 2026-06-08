
from dataclasses import dataclass
from decimal import Decimal


@dataclass(eq=True, frozen=True)
class Volume:
    """
    Volume in litres
    """
    value: Decimal


    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Volume can't be negative or zero")
