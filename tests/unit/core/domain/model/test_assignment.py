import uuid

import pytest

from src.core.domain.model.assignment import Assignment, AssignmentStatusEnum
from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume


def test_complete_assignment_sets_status_to_completed():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))

    result = assignment.complete_assignment(courier_location=Location(x=1, y=4))
    assert result.is_success()
    assert assignment.status == AssignmentStatusEnum.COMPLETED


def test_cant_complete_assignment_twice():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))
    assignment.complete_assignment(courier_location=Location(x=1, y=4))

    result = assignment.complete_assignment(courier_location=Location(x=1, y=4))
    assert result.is_failure()
    assert result.get_error().message == "Assignment already completed"


@pytest.mark.parametrize(
    "courier_location,should_succeed",
    [
        pytest.param(Location(x=5, y=5), True, id="same_location"),
        pytest.param(Location(x=5, y=6), True, id="adjacent"),
        pytest.param(Location(x=5, y=7), False, id="too_far"),
    ]
)
def test_complete_assignment_distance_validation(courier_location, should_succeed):
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=5, y=5))

    if should_succeed:
        result = assignment.complete_assignment(courier_location=courier_location)
        assert result.is_success()
        assert assignment.status == AssignmentStatusEnum.COMPLETED
    else:
        result = assignment.complete_assignment(courier_location=courier_location)
        assert result.is_failure()
        assert result.get_error().message == "Courier has to be nearby assignment"


def test_assignment_with_same_id_is_equal():
    uuid_1 = uuid.uuid4()
    assignment_1 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))
    assignment_2 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(_value=51), location=Location(x=2, y=3))

    assert assignment_1 == assignment_2


def test_assignment_with_different_id_not_equal():
    uuid_1 = uuid.uuid4()
    uuid_2 = uuid.uuid4()
    assignment_1 = Assignment(id=uuid_1, order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))
    assignment_2 = Assignment(id=uuid_2, order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))

    assert assignment_1 != assignment_2


def test_assignment_comparison_with_non_assignment_raises_error():
    assignment = Assignment(id=uuid.uuid4(), order_id=uuid.uuid4(), volume=Volume(_value=1), location=Location(x=1, y=4))

    with pytest.raises(NotImplementedError):
        assignment == "not an assignment"
