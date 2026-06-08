from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from src.core.domain.model.volume import Volume


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(-1, id='negative'),
        pytest.param(0, id='zero'),
        pytest.param(-0.5, id='negative_decimal'),
    ]
)
def test_volume_incorrect_value_raises_error(value: float):
    with pytest.raises(ValueError):
        Volume(Decimal(value))


def test_same_volumes_equal():
    assert Volume(Decimal(1)) == Volume(Decimal(1))
    assert Volume(Decimal("2.5")) == Volume(Decimal("2.5"))


def test_volume_mutation_forbidden():
    volume = Volume(Decimal(1))
    with pytest.raises(FrozenInstanceError):
        volume.value = Decimal(2)


@pytest.mark.parametrize(
    "volume_1, volume_2",
    [
        pytest.param(Volume(Decimal(1)), Volume(Decimal(2)), id='different_values'),
        pytest.param(Volume(Decimal("2.5")), Volume(Decimal("3.5")), id='different_decimal_values'),
        pytest.param(Volume(Decimal(1)), Volume(Decimal("1.5")), id='integer_vs_decimal'),
    ]
)
def test_volumes_not_equal(volume_1: Volume, volume_2: Volume):
    assert volume_1 != volume_2
