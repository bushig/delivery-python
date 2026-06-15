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
def test_volume_incorrect_value_returns_failure(value: float):
    result = Volume.create(value=Decimal(value))
    assert result.is_failure()


def test_volume_create_success():
    result = Volume.create(value=Decimal(10))
    assert result.is_success()
    assert result.get_value() == Volume(value=Decimal(10))


def test_same_volumes_equal():
    assert Volume(value=Decimal(1)) == Volume(value=Decimal(1))
    assert Volume(value=Decimal("2.5")) == Volume(value=Decimal("2.5"))


def test_volume_mutation_forbidden():
    volume = Volume(value=Decimal(1))
    with pytest.raises(FrozenInstanceError):
        volume.value = Decimal(2)


@pytest.mark.parametrize(
    "volume_1, volume_2",
    [
        pytest.param(Volume(value=Decimal(1)), Volume(value=Decimal(2)), id='different_values'),
        pytest.param(Volume(value=Decimal("2.5")), Volume(value=Decimal("3.5")), id='different_decimal_values'),
        pytest.param(Volume(value=Decimal(1)), Volume(value=Decimal("1.5")), id='integer_vs_decimal'),
    ]
)
def test_volumes_not_equal(volume_1: Volume, volume_2: Volume):
    assert volume_1 != volume_2


def test_volume_add():
    v1 = Volume(value=Decimal(10))
    v2 = Volume(value=Decimal(5))
    result = v1 + v2
    assert result == Volume(value=Decimal(15))


def test_volume_add_commutative():
    v1 = Volume(value=Decimal(10))
    v2 = Volume(value=Decimal(5))
    assert v1 + v2 == v2 + v1


def test_volume_sum_volumes():
    volumes = [
        Volume(value=Decimal(10)),
        Volume(value=Decimal(5)),
        Volume(value=Decimal(3)),
    ]
    result = Volume.sum_volumes(volumes)
    assert result == Volume(value=Decimal(18))


def test_volume_sum_volumes_empty():
    with pytest.raises(TypeError, match="reduce.*empty iterable"):
        Volume.sum_volumes([])


@pytest.mark.parametrize(
    "v1, v2, expected",
    [
        pytest.param(Volume(Decimal(10)), Volume(Decimal(5)), True, id='greater'),
        pytest.param(Volume(Decimal(5)), Volume(Decimal(10)), False, id='less'),
        pytest.param(Volume(Decimal(10)), Volume(Decimal(10)), False, id='equal'),
    ]
)
def test_volume_greater_than(v1, v2, expected):
    assert (v1 > v2) == expected


@pytest.mark.parametrize(
    "v1, v2, expected",
    [
        pytest.param(Volume(Decimal(10)), Volume(Decimal(5)), False, id='less'),
        pytest.param(Volume(Decimal(5)), Volume(Decimal(10)), True, id='greater'),
        pytest.param(Volume(Decimal(10)), Volume(Decimal(10)), True, id='equal'),
    ]
)
def test_volume_less_or_equal(v1, v2, expected):
    assert (v1 <= v2) == expected
