from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from src.adapters.out.postgres.database import Database
from src.adapters.out.postgres.unit_of_work import UnitOfWorkImpl
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume


def _make_order() -> OrderAggregate:
    return OrderAggregate(
        id=uuid4(),
        location=Location(x=3, y=3),
        volume=Volume(_value=Decimal("5.0")),
        status=OrderStatusEnum.CREATED,
    )


def _make_courier(name: str = "Courier") -> CourierAggregate:
    return CourierAggregate(
        name=name,
        location=Location(x=1, y=1),
        max_volume=Volume(_value=Decimal("20.0")),
    )


async def test_commit_saves_both_aggregates(database: Database) -> None:
    order = _make_order()
    courier = _make_courier()

    async with UnitOfWorkImpl(database) as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    async with UnitOfWorkImpl(database) as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_courier is not None
    assert saved_courier.id == courier.id


async def test_rollback_on_exception(database: Database) -> None:
    order = _make_order()
    courier = _make_courier()

    try:
        async with UnitOfWorkImpl(database) as uow:
            await uow.orders.add(order)
            await uow.couriers.add(courier)
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    async with UnitOfWorkImpl(database) as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is None
    assert saved_courier is None
