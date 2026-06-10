from pydantic import BaseModel, ConfigDict

MIN_X = 1
MAX_X = 10
MIN_Y = 1
MAX_Y = 10


class Location(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int
    y: int

    def model_post_init(self, __context: object) -> None:
        self.check_is_valid_coordinates(self.x, self.y)

    def calculate_distance(self, other_location: "Location") -> int:
        return abs(self.x - other_location.x) + abs(self.y - other_location.y)

    @staticmethod
    def check_is_valid_coordinates(x: int, y: int) -> None:
        if x < MIN_X or x > MAX_X:
            raise ValueError(f"x must be between {MIN_X} and {MAX_X}")
        if y < MIN_Y or y > MAX_Y:
            raise ValueError(f"y must be between {MIN_Y} and {MAX_Y}")
