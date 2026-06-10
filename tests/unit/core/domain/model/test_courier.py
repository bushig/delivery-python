
import uuid

import pytest

from src.core.domain.model.assignment import Assignment
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume


def test_can_take_order_when_volume_fits():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    result = courier.can_take_order(order)

    assert result is True


def test_cant_take_order_when_volume_exceeds_max():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(25))

    result = courier.can_take_order(order)

    assert result is False


def test_can_take_order_with_existing_assignments():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    existing_order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    courier.take_order(existing_order)

    new_order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(5))

    result = courier.can_take_order(new_order)

    assert result is True


def test_take_order_creates_assignment_and_adds_to_list():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    courier.take_order(order)

    assert len(courier.assignments) == 1
    assert courier.assignments[0].order_id == order.id
    assert courier.assignments[0].volume == order.volume
    assert courier.assignments[0].location == order.location


def test_take_order_raises_when_volume_exceeds():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(25))

    with pytest.raises(ValueError, match="cant take assignment - too big"):
        courier.take_order(order)


def test_complete_assignment_succeeds_when_courier_nearby():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    courier.take_order(order)
    assignment = courier.assignments[0]

    courier.complete_assignment(assignment)

    assert assignment.status.name == "completed"


def test_complete_assignment_raises_when_assignment_not_in_list():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    assignment = Assignment.create_from_order(order)

    with pytest.raises(ValueError, match="cant complete assignment - not in assignment list"):
        courier.complete_assignment(assignment)


def test_complete_assignment_raises_when_courier_too_far():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(1, 1), max_volume=Volume(20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    courier.take_order(order)
    assignment = courier.assignments[0]

    with pytest.raises(ValueError, match="cant complete assignment - too far away"):
        courier.complete_assignment(assignment)


def test_change_location_updates_location():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )
    new_location = Location(3, 3)

    courier.change_location(new_location)

    assert courier.location == new_location


def test_change_location_raises_for_invalid_coordinates():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(5, 5), max_volume=Volume(20)
    )

    with pytest.raises(ValueError):
        courier.change_location(Location(999, 999))
