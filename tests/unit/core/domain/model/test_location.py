

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
def test_location_incorrect_values_raises_error(x: int, y: int):
    with pytest.raises(ValueError):
        Location(x, y)



def test_same_locations_equal():
     assert Location(1, 4) == Location(1, 4)

def test_location_mutation_forbidden():
     location = Location(1, 4)
     with pytest.raises(FrozenInstanceError):
        location.x = 1


@pytest.mark.parametrize(
        "location_1,location_2",
        [
        pytest.param(Location(2, 4), Location(1, 4), id='x_different'),
        pytest.param(Location(2, 4), Location(2, 5), id='y_different'),
        pytest.param(Location(2, 4), Location(1, 4), id='both_different'),
        ]


)
def test_locations_not_equal(location_1: Location, location_2: Location):
     assert location_1 != location_2


@pytest.mark.parametrize(
        "location_1,location_2,distance",
        [
        pytest.param(Location(2, 4), Location(2, 4), 0, id='zero_distance'),
        pytest.param(Location(2, 4), Location(2, 5), 1, id='y_differs_bigger'),
        pytest.param(Location(2, 4), Location(2, 2), 2, id='y_differs_smaller'),
        pytest.param(Location(1, 1), Location(4, 4), 6, id='y_differs_smaller'),
        ]


)
def test_locations_distance(location_1: Location, location_2: Location, distance: int):
     assert location_1.calculate_distance(location_2) == distance

