from __future__ import annotations

from tests.factories import CourierAggregateFactory, OrderAggregateFactory


async def test_commit_saves_both_aggregates(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build()
    courier = CourierAggregateFactory.build()

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_courier is not None
    assert saved_courier.id == courier.id


async def test_rollback_on_exception(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build()
    courier = CourierAggregateFactory.build()

    try:
        async with unit_of_work_factory() as uow:
            await uow.orders.add(order)
            await uow.couriers.add(courier)
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is None
    assert saved_courier is None
