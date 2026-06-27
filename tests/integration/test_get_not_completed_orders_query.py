from __future__ import annotations

from src.core.application.queries.get_not_completed_orders import get_not_completed_orders
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderStatusEnum
from tests.factories import OrderAggregateFactory


async def test_get_not_completed_orders_returns_created_and_assigned(unit_of_work_factory) -> None:
    order_created = OrderAggregateFactory.build(status=OrderStatusEnum.CREATED, location=Location(x=1, y=1))
    order_assigned = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED, location=Location(x=2, y=2))
    order_completed = OrderAggregateFactory.build(status=OrderStatusEnum.COMPLETED, location=Location(x=3, y=3))

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order_created)
        await uow.orders.add(order_assigned)
        await uow.orders.add(order_completed)
        await uow.commit()

    async with unit_of_work_factory() as uow:
        result = await get_not_completed_orders(uow)

    assert len(result) == 2

    returned_ids = {dto.id for dto in result}
    assert returned_ids == {order_created.id, order_assigned.id}

    locations = {(dto.location.x, dto.location.y) for dto in result}
    assert locations == {(1, 1), (2, 2)}


async def test_get_not_completed_orders_empty(unit_of_work_factory) -> None:
    async with unit_of_work_factory() as uow:
        result = await get_not_completed_orders(uow)

    assert len(result) == 0


async def test_get_not_completed_orders_only_completed(unit_of_work_factory) -> None:
    order_completed = OrderAggregateFactory.build(status=OrderStatusEnum.COMPLETED)

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order_completed)
        await uow.commit()

    async with unit_of_work_factory() as uow:
        result = await get_not_completed_orders(uow)

    assert len(result) == 0
