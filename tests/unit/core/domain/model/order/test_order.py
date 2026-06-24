
import uuid

import pytest

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume


def test_order_default_status_is_created():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(_value=10))

    assert order.status == OrderStatusEnum.CREATED


@pytest.mark.parametrize(
    "initial_status,new_status,should_succeed,error_match",
    [
        pytest.param(
            OrderStatusEnum.CREATED, OrderStatusEnum.ASSIGNED, True, None, id="created_to_assigned"
        ),
        pytest.param(
            OrderStatusEnum.ASSIGNED, OrderStatusEnum.COMPLETED, True, None, id="assigned_to_completed"
        ),
        pytest.param(
            OrderStatusEnum.ASSIGNED,
            OrderStatusEnum.ASSIGNED,
            False,
            "Order can be assigned only if it is in status 'Created'",
            id="cant_assign_from_assigned",
        ),
        pytest.param(
            OrderStatusEnum.CREATED,
            OrderStatusEnum.COMPLETED,
            False,
            "Order can be completed only if it is in status 'Assigned'",
            id="cant_complete_from_created",
        ),
        pytest.param(
            OrderStatusEnum.CREATED, "InvalidStatus", False, "Cant change to this status", id="invalid_status"
        ),
    ]
)
def test_change_status_transitions(initial_status, new_status, should_succeed, error_match):
    order = OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(_value=10), status=initial_status)

    if should_succeed:
        result = order.change_status(new_status)
        assert result.is_success()
        assert order.status == new_status
    else:
        result = order.change_status(new_status)
        assert result.is_failure()
        assert result.get_error().message == error_match
