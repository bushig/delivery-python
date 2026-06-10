
import uuid

import pytest

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume


def test_order_default_status_is_created():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    assert order.status == OrderStatusEnum.created


def test_change_status_to_assigned_from_created():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    order.change_status(OrderStatusEnum.assigned)

    assert order.status == OrderStatusEnum.assigned


def test_change_status_to_completed_from_assigned():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    order.change_status(OrderStatusEnum.assigned)

    order.change_status(OrderStatusEnum.completed)

    assert order.status == OrderStatusEnum.completed


def test_cant_assign_order_not_in_created_status():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))
    order.change_status(OrderStatusEnum.assigned)

    with pytest.raises(ValueError, match="Order can be assigned only if it is in status 'Created'"):
        order.change_status(OrderStatusEnum.assigned)


def test_cant_complete_order_not_in_assigned_status():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    with pytest.raises(ValueError, match="Order can be completed only if it is in status 'Assigned'"):
        order.change_status(OrderStatusEnum.completed)


def test_cant_change_to_invalid_status():
    order = OrderAggregate(id=uuid.uuid4(), location=Location(5, 5), volume=Volume(10))

    with pytest.raises(ValueError, match="Cant change to this status"):
        order.change_status("InvalidStatus")
