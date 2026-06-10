import uuid

import pytest

from src.core.domain.model.assignment import Assignment, AssignmentStatusEnum
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume


def test_create_from_order_creates_assignment_with_order_data():
    order_id = uuid.uuid4()
    order_location = Location(x=5, y=5)
    order_volume = Volume(value=10)
    order = OrderAggregate(id=order_id, location=order_location, volume=order_volume)

    assignment = Assignment.create_from_order(order)

    assert assignment.order_id == order_id
    assert assignment.location == order_location
    assert assignment.volume == order_volume


def test_create_from_order_sets_default_status_assigned():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))

    assignment = Assignment.create_from_order(order)

    assert assignment.status == AssignmentStatusEnum.assigned


def test_create_from_order_generates_unique_id():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(value=10))

    assignment_1 = Assignment.create_from_order(order)
    assignment_2 = Assignment.create_from_order(order)

    assert assignment_1.id != assignment_2.id


def test_complete_assignment_sets_status_to_completed():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=1, y=4))

    assignment.complete_assignment(courier_location=Location(x=1, y=4))

    assert assignment.status == AssignmentStatusEnum.completed


def test_cant_complete_assignment_twice():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=1, y=4))
    assignment.complete_assignment(courier_location=Location(x=1, y=4))

    with pytest.raises(ValueError, match="Assignment already completed"):
        assignment.complete_assignment(courier_location=Location(x=1, y=4))


@pytest.mark.parametrize(
    "courier_location,should_succeed",
    [
        pytest.param(Location(x=5, y=5), True, id="same_location"),
        pytest.param(Location(x=5, y=6), True, id="adjacent"),
        pytest.param(Location(x=5, y=7), False, id="too_far"),
    ]
)
def test_complete_assignment_distance_validation(courier_location, should_succeed):
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=5, y=5))

    if should_succeed:
        assignment.complete_assignment(courier_location=courier_location)
        assert assignment.status == AssignmentStatusEnum.completed
    else:
        with pytest.raises(ValueError, match="Courier has to be in same location as assignment"):
            assignment.complete_assignment(courier_location=courier_location)


def test_assignment_with_same_id_is_equal():
    uuid_1 = uuid.uuid4()
    assignment_1 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=1, y=4))
    assignment_2 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(value=51), location=Location(x=2, y=3))

    assert assignment_1 == assignment_2


def test_assignment_with_different_id_not_equal():
    uuid_1 = uuid.uuid4()
    uuid_2 = uuid.uuid4()
    assignment_1 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=1, y=4))
    assignment_2 = Assignment(id=uuid_2, order_id=uuid.uuid4(), volume=Volume(value=1), location=Location(x=1, y=4))

    assert assignment_1 != assignment_2
