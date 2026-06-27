from __future__ import annotations

from src.adapters.out.postgres.database import Database
from src.adapters.out.postgres.unit_of_work import UnitOfWorkPostgres
from tests.factories import CourierAggregateFactory, OrderAggregateFactory


async def test_commit_saves_both_aggregates(database: Database) -> None:
    order = OrderAggregateFactory.build()
    courier = CourierAggregateFactory.build()

    async with UnitOfWorkPostgres(database) as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    async with UnitOfWorkPostgres(database) as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_courier is not None
    assert saved_courier.id == courier.id


async def test_rollback_on_exception(database: Database) -> None:
    order = OrderAggregateFactory.build()
    courier = CourierAggregateFactory.build()

    try:
        async with UnitOfWorkPostgres(database) as uow:
            await uow.orders.add(order)
            await uow.couriers.add(courier)
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    async with UnitOfWorkPostgres(database) as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is None
    assert saved_courier is None
