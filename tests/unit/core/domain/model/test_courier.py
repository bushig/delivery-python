
import uuid

import pytest

from src.core.domain.model.assignment import AssignmentStatusEnum
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume


@pytest.mark.parametrize(
    "existing_volumes,new_volume,max_volume,expected",
    [
        pytest.param([], 10, 20, True, id="no_assignments_fits"),
        pytest.param([], 25, 20, False, id="no_assignments_exceeds"),
        pytest.param([], 20, 20, True, id="exact_max_volume"),
        pytest.param([12], 10, 20, False, id="with_existing_exceeds"),
        pytest.param([10], 5, 20, True, id="with_existing_fits"),
    ]
)
def test_can_take_order_volume_check(existing_volumes, new_volume, max_volume, expected):
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=max_volume)
    )
    for vol in existing_volumes:
        order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=vol))
        courier.take_order(order)

    new_order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=new_volume))

    result = courier.can_take_order(new_order)

    assert result is expected


def test_take_order_creates_assignment_and_adds_to_list():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))

    courier.take_order(order)

    assert len(courier.assignments) == 1
    assert courier.assignments[0].order_id == order.id
    assert courier.assignments[0].volume == order.volume
    assert courier.assignments[0].location == order.location


def test_take_order_returns_failure_when_volume_exceeds():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=25))

    result = courier.take_order(order)

    assert result.is_failure()
    assert result.get_error().message == "cant take assignment - too big"


def test_complete_assignment_succeeds_when_courier_nearby():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(order)
    assignment_id = courier.assignments[0].id

    result = courier.complete_assignment(assignment_id)

    assert result.is_success()
    assert courier.assignments[0].status.name == "completed"


def test_complete_assignment_returns_failure_when_assignment_not_in_list():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(order)
    fake_assignment_id = uuid.uuid4()

    result = courier.complete_assignment(fake_assignment_id)

    assert result.is_failure()
    assert result.get_error().message == "cant complete assignment - not in assignment list"


def test_complete_assignment_returns_failure_when_courier_too_far():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=1, y=1), _max_volume=Volume(value=20)
    )
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))
    courier.take_order(order)
    assignment_id = courier.assignments[0].id

    result = courier.complete_assignment(assignment_id)

    assert result.is_failure()
    assert result.get_error().message == "cant complete assignment - too far away"


def test_change_location_updates_location():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    new_location = Location(x=3, y=3)

    courier.change_location(new_location)

    assert courier.location == new_location


def test_default_max_volume_is_20():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5)
    )

    assert courier.max_volume == Volume(value=20)


def test_can_take_order_after_completing_assignment():
    courier = CourierAggregate(
        _id=uuid.uuid4(), _name="Test Courier", _location=Location(x=5, y=5), _max_volume=Volume(value=20)
    )
    order1 = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=15))
    courier.take_order(order1)
    assignment_id = courier.assignments[0].id
    courier.complete_assignment(assignment_id)

    order2 = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=15))

    assert courier.can_take_order(order2) is True
