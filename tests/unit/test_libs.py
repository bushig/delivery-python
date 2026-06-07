import pytest

from delivery.libs.ddd import ValueObject
from delivery.libs.errs import DomainInvariantException, Guard


class TestValueObject:
    def test_equality_by_components(self):
        class Point(ValueObject):
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

            def equality_components(self) -> tuple:
                return (self.x, self.y)

        assert Point(1, 2) == Point(1, 2)
        assert Point(1, 2) != Point(3, 4)

    def test_hash_by_components(self):
        class Point(ValueObject):
            def __init__(self, x: int, y: int):
                self.x = x
                self.y = y

            def equality_components(self) -> tuple:
                return (self.x, self.y)

        assert hash(Point(1, 2)) == hash(Point(1, 2))
        assert {Point(1, 2), Point(1, 2)} == {Point(1, 2)}


class TestGuard:
    def test_against_null_or_empty_string(self):
        Guard.against_null_or_empty("hello", "field")
        with pytest.raises(DomainInvariantException):
            Guard.against_null_or_empty("", "field")
        with pytest.raises(DomainInvariantException):
            Guard.against_null_or_empty(None, "field")

    def test_against_out_of_range(self):
        Guard.against_out_of_range(5, 0, 10, "field")
        with pytest.raises(DomainInvariantException):
            Guard.against_out_of_range(15, 0, 10, "field")
