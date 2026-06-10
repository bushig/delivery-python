

import uuid

import pytest

from src.core.domain.model.assignment import Assignment, AssignmentStatusEnum
from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume


def test_assignment_with_same_id_is_equal():
    uuid_1 = uuid.uuid4()
    assignment_1 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(1), location=Location(1, 4))

    assignment_2 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(51), location=Location(2, 3))
    assert assignment_1 == assignment_2


def test_cant_complete_same_assignment_twice():
    assignment_1 = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(1), location=Location(1, 4))

    assignment_1.complete_assignment(courier_location=Location(1, 4))
    with pytest.raises(ValueError):
        assignment_1.complete_assignment(courier_location=Location(1, 4))

def test_assignment_completion_set_correct_status():
    assignment_1 = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(1), location=Location(1, 4))

    assignment_1.complete_assignment(courier_location=Location(1, 4))
    assert assignment_1.status == AssignmentStatusEnum.completed


def test_can_complete_when_courier_is_adjacent_or_at_location():
    order_location = Location(5, 5)
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(1), location=order_location)

    assignment.complete_assignment(courier_location=Location(5, 5))
    assert assignment.status == AssignmentStatusEnum.completed

    assignment_2 = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(1), location=order_location)
    assignment_2.complete_assignment(courier_location=Location(5, 6))
    assert assignment_2.status == AssignmentStatusEnum.completed


def test_cant_complete_when_courier_is_too_far():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(1), location=Location(5, 5))

    with pytest.raises(ValueError):
        assignment.complete_assignment(courier_location=Location(5, 7))

