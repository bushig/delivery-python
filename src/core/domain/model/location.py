from dataclasses import dataclass

MIN_X = 1
MAX_X = 10
MIN_Y = 1
MAX_Y = 10


@dataclass(eq=True, frozen=True)
class Location:
    x: int
    y: int


    def __post_init__(self):
        self.check_is_valid_coordinates(self.x, self.y)


    def calculate_distance(self, other_location: "Location") -> int:
        """
        returns numbers of steps required to get to this point
        """
        return abs(self.x - other_location.x) + abs(self.y-other_location.y)

    @staticmethod
    def check_is_valid_coordinates(x: int, y: int) -> None:
        if x < MIN_X or x > MAX_X:
            raise ValueError(f"x must be between {MIN_X} and {MAX_X}")
        if y < MIN_Y or y > MAX_Y:
            raise ValueError(f"y must be between {MIN_Y} and {MAX_Y}")

