from dataclasses import dataclass
from decimal import Decimal
from functools import reduce
from operator import add

from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import ValueIsInvalidError
from src.libs.errs.result import Result


@dataclass(frozen=True)
class Volume:
    value: Decimal

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Volume can't be negative or zero")

    @staticmethod
    def create(value: Decimal) -> Result["Volume", DomainError]:
        try:
            return Result.success(Volume(value=value))
        except ValueError as e:
            return Result.failure(ValueIsInvalidError(message=str(e)))

    def __add__(self, other: "Volume") -> "Volume":
        return Volume(value=self.value + other.value)

    def __le__(self, other: "Volume") -> bool:
        return self.value <= other.value

    def __lt__(self, other: "Volume") -> bool:
        return self.value < other.value

    def __gt__(self, other: "Volume") -> bool:
        return self.value > other.value

    def __ge__(self, other: "Volume") -> bool:
        return self.value >= other.value

    @staticmethod
    def sum_volumes(volumes: list["Volume"]) -> "Volume":
        return reduce(add, volumes)
