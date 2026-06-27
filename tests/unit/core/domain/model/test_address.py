from dataclasses import FrozenInstanceError

import pytest

from src.core.domain.model.address import Address


@pytest.mark.parametrize(
    "country,city,street,house,apartment",
    [
        pytest.param("", "Moscow", "Tverskaya", "10", "5", id="country_empty"),
        pytest.param("Russia", "", "Tverskaya", "10", "5", id="city_empty"),
        pytest.param("Russia", "Moscow", "", "10", "5", id="street_empty"),
        pytest.param("Russia", "Moscow", "Tverskaya", "", "5", id="house_empty"),
        pytest.param("Russia", "Moscow", "Tverskaya", "10", "", id="apartment_empty"),
    ],
)
def test_address_empty_field_raises_value_error(country, city, street, house, apartment):
    with pytest.raises(ValueError):
        Address(
            country=country,
            city=city,
            street=street,
            house=house,
            apartment=apartment,
        )


def test_address_create_success():
    address = Address(
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house="10",
        apartment="5",
    )
    assert address.country == "Russia"
    assert address.city == "Moscow"
    assert address.street == "Tverskaya"
    assert address.house == "10"
    assert address.apartment == "5"


def test_address_mutation_forbidden():
    address = Address(
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house="10",
        apartment="5",
    )
    with pytest.raises(FrozenInstanceError):
        address.country = "USA"


def test_same_addresses_equal():
    address1 = Address(
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house="10",
        apartment="5",
    )
    address2 = Address(
        country="Russia",
        city="Moscow",
        street="Tverskaya",
        house="10",
        apartment="5",
    )
    assert address1 == address2


@pytest.mark.parametrize(
    "address1,address2",
    [
        pytest.param(
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            Address(country="USA", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            id="country_different",
        ),
        pytest.param(
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            Address(country="Russia", city="SPb", street="Tverskaya", house="10", apartment="5"),
            id="city_different",
        ),
        pytest.param(
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            Address(country="Russia", city="Moscow", street="Lenina", house="10", apartment="5"),
            id="street_different",
        ),
        pytest.param(
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            Address(country="Russia", city="Moscow", street="Tverskaya", house="15", apartment="5"),
            id="house_different",
        ),
        pytest.param(
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="5"),
            Address(country="Russia", city="Moscow", street="Tverskaya", house="10", apartment="10"),
            id="apartment_different",
        ),
    ],
)
def test_addresses_not_equal(address1: Address, address2: Address):
    assert address1 != address2
