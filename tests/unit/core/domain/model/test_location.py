from dataclasses import FrozenInstanceError

import pytest

from src.core.domain.model.location import Location


@pytest.mark.parametrize(
        "x,y",
        [
        pytest.param(-1, 0, id='x_negative'),
        pytest.param(1, -4, id='y_negative'),
        pytest.param(-1, -3, id='all_negative'),
        pytest.param(999, 3, id='x_too_big'),
        pytest.param(0, 513, id='y_too_big'),
        pytest.param(999, 324, id='all_too_big'),
        ]

)
def test_location_incorrect_values_returns_failure(x: int, y: int):
    result = Location.create(x=x, y=y)
    assert result.is_failure()


def test_location_create_success():
    result = Location.create(x=5, y=5)
    assert result.is_success()
    assert result.get_value().x == 5
    assert result.get_value().y == 5


def test_same_locations_equal():
     assert Location(x=1, y=4) == Location(x=1, y=4)

def test_location_mutation_forbidden():
     location = Location(x=1, y=4)
     with pytest.raises(FrozenInstanceError):
        location.x = 1


@pytest.mark.parametrize(
        "location_1,location_2",
        [
        pytest.param(Location(x=2, y=4), Location(x=1, y=4), id='x_different'),
        pytest.param(Location(x=2, y=4), Location(x=2, y=5), id='y_different'),
        pytest.param(Location(x=2, y=4), Location(x=1, y=4), id='both_different'),
        ]


)
def test_locations_not_equal(location_1: Location, location_2: Location):
     assert location_1 != location_2


@pytest.mark.parametrize(
        "location_1,location_2,distance",
        [
        pytest.param(Location(x=2, y=4), Location(x=2, y=4), 0, id='zero_distance'),
        pytest.param(Location(x=2, y=4), Location(x=2, y=5), 1, id='y_differs_bigger'),
        pytest.param(Location(x=2, y=4), Location(x=2, y=2), 2, id='y_differs_smaller'),
        pytest.param(Location(x=1, y=1), Location(x=4, y=4), 6, id='y_differs_smaller'),
        ]


)
def test_locations_distance(location_1: Location, location_2: Location, distance: int):
     assert location_1.calculate_distance(location_2) == distance


def test_location_generate_random():
    location = Location.generate_random()

    assert isinstance(location, Location)
    assert 1 <= location.x <= 10
    assert 1 <= location.y <= 10
