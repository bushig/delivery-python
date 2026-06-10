
import uuid

import pytest

from src.core.domain.model.assignment import Assignment
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate as Order
from src.core.domain.model.volume import Volume


@pytest.mark.parametrize(
    "order_volume,max_volume,expected",
    [
        pytest.param(10, 20, True, id="volume_fits"),
        pytest.param(25, 20, False, id="volume_exceeds"),
    ]
)
def test_can_take_order_volume_check(order_volume, max_volume, expected):
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=max_volume)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=order_volume))

    result = courier.can_take_order(order)

    assert result is expected


def test_can_take_order_with_existing_assignments():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    existing_order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(existing_order)

    new_order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=5))

    result = courier.can_take_order(new_order)

    assert result is True


def test_take_order_creates_assignment_and_adds_to_list():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))

    courier.take_order(order)

    assert len(courier.assignments) == 1
    assert courier.assignments[0].order_id == order.id
    assert courier.assignments[0].volume == order.volume
    assert courier.assignments[0].location == order.location


def test_take_order_returns_failure_when_volume_exceeds():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=25))

    result = courier.take_order(order)

    assert result.is_failure()
    assert result.get_error().message == "cant take assignment - too big"


def test_complete_assignment_succeeds_when_courier_nearby():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(order)
    assignment = courier.assignments[0]

    result = courier.complete_assignment(assignment)

    assert result.is_success()
    assert assignment.status.name == "completed"


def test_complete_assignment_returns_failure_when_assignment_not_in_list():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    assignment = Assignment.create_from_order(order)

    result = courier.complete_assignment(assignment)

    assert result.is_failure()
    assert result.get_error().message == "cant complete assignment - not in assignment list"


def test_complete_assignment_returns_failure_when_courier_too_far():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=1, y=1), max_volume=Volume(value=20)
    )
    order = Order(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(order)
    assignment = courier.assignments[0]

    result = courier.complete_assignment(assignment)

    assert result.is_failure()
    assert result.get_error().message == "cant complete assignment - too far away"


def test_change_location_updates_location():
    courier = CourierAggregate(
        id=uuid.uuid4(), name="Test Courier", location=Location(x=5, y=5), max_volume=Volume(value=20)
    )
    new_location = Location(x=3, y=3)

    courier.change_location(new_location)

    assert courier.location == new_location
