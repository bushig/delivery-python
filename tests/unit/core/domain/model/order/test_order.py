
import uuid

import pytest

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume


def test_order_default_status_is_created():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    assert order.status == OrderStatusEnum.created


@pytest.mark.parametrize(
    "initial_status,new_status,should_succeed,error_match",
    [
        pytest.param(
            OrderStatusEnum.created, OrderStatusEnum.assigned, True, None, id="created_to_assigned"
        ),
        pytest.param(
            OrderStatusEnum.assigned, OrderStatusEnum.completed, True, None, id="assigned_to_completed"
        ),
        pytest.param(
            OrderStatusEnum.assigned,
            OrderStatusEnum.assigned,
            False,
            "Order can be assigned only if it is in status 'Created'",
            id="cant_assign_from_assigned",
        ),
        pytest.param(
            OrderStatusEnum.created,
            OrderStatusEnum.completed,
            False,
            "Order can be completed only if it is in status 'Assigned'",
            id="cant_complete_from_created",
        ),
        pytest.param(
            OrderStatusEnum.created, "InvalidStatus", False, "Cant change to this status", id="invalid_status"
        ),
    ]
)
def test_change_status_transitions(initial_status, new_status, should_succeed, error_match):
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10), status=initial_status)

    if should_succeed:
        order.change_status(new_status)
        assert order.status == new_status
    else:
        with pytest.raises(ValueError, match=error_match):
            order.change_status(new_status)
