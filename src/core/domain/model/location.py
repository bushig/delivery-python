from dataclasses import dataclass

from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import ValueIsOutOfRangeError
from src.libs.errs.result import Result

MIN_X = 1
MAX_X = 10
MIN_Y = 1
MAX_Y = 10


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def __post_init__(self):
        if not (MIN_X <= self.x <= MAX_X):
            raise ValueError(f"x must be between {MIN_X} and {MAX_X}")
        if not (MIN_Y <= self.y <= MAX_Y):
            raise ValueError(f"y must be between {MIN_Y} and {MAX_Y}")

    def calculate_distance(self, other_location: "Location") -> int:
        return abs(self.x - other_location.x) + abs(self.y - other_location.y)

    @staticmethod
    def create(x: int, y: int) -> Result["Location", DomainError]:
        if x < MIN_X or x > MAX_X:
            return Result.failure(ValueIsOutOfRangeError(message=f"x must be between {MIN_X} and {MAX_X}"))
        if y < MIN_Y or y > MAX_Y:
            return Result.failure(ValueIsOutOfRangeError(message=f"y must be between {MIN_Y} and {MAX_Y}"))
        return Result.success(Location(x=x, y=y))
