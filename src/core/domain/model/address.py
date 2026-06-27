
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Address:
    country: str
    city: str
    street: str
    house: str
    apartment: str

    def __post_init__(self):
        if not self.country:
            raise ValueError("country is required")
        if not self.city:
            raise ValueError("city is required")
        if not self.street:
            raise ValueError("street is required")
        if not self.house:
            raise ValueError("house is required")
        if not self.apartment:
            raise ValueError("apartment is required")



