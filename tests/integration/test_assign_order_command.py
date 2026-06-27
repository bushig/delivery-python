from __future__ import annotations

from decimal import Decimal

import pytest

from src.adapters.out.postgres.unit_of_work import UnitOfWorkPostgres
from src.core.application.commands.assign_order_to_courier import AssignOrderCommand, assign_order
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderStatusEnum
from src.core.domain.model.volume import Volume
from src.core.domain.services.dispatch_service import DispatchDomainService
from src.libs.errs.exceptions import DomainInvariantException
from tests.factories import CourierAggregateFactory, OrderAggregateFactory


async def test_assign_order_success(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build()
    courier = CourierAggregateFactory.build(name="Test Courier", location=Location(x=3, y=3))

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = AssignOrderCommand()
    dispatch_service = DispatchDomainService()
    async with unit_of_work_factory() as uow:
        await assign_order(cmd, uow, dispatch_service)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatusEnum.ASSIGNED
    assert saved_courier is not None
    assert len(saved_courier.assignments) == 1
    assert saved_courier.assignments[0].order_id == order.id


async def test_assign_order_no_orders(unit_of_work_factory) -> None:
    courier = CourierAggregateFactory.build()
    async with unit_of_work_factory() as uow:
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = AssignOrderCommand()
    dispatch_service = DispatchDomainService()
    async with unit_of_work_factory() as uow:
        await assign_order(cmd, uow, dispatch_service)

    async with unit_of_work_factory() as uow:
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_courier is not None
    assert len(saved_courier.assignments) == 0


async def test_assign_order_no_suitable_couriers(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build(volume=Volume(_value=Decimal("10.0")))
    courier = CourierAggregateFactory.build(name="Overloaded Courier")
    existing_order = OrderAggregateFactory.build(volume=Volume(_value=Decimal("15.0")))

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.orders.add(existing_order)
        await uow.couriers.add(courier)
        await uow.commit()

    courier.take_order(existing_order)
    async with unit_of_work_factory() as uow:
        await uow.couriers.update(courier)
        await uow.commit()

    cmd = AssignOrderCommand()
    dispatch_service = DispatchDomainService()

    with pytest.raises(DomainInvariantException):
        async with unit_of_work_factory() as uow:
            await assign_order(cmd, uow, dispatch_service)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatusEnum.CREATED


async def test_assign_order_empty_couriers_list(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build()

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.commit()

    cmd = AssignOrderCommand()
    dispatch_service = DispatchDomainService()

    with pytest.raises(DomainInvariantException):
        async with unit_of_work_factory() as uow:
            await assign_order(cmd, uow, dispatch_service)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatusEnum.CREATED


async def test_assign_order_chooses_nearest_courier(unit_of_work_factory) -> None:
    order = OrderAggregateFactory.build(location=Location(x=5, y=5))
    courier_far = CourierAggregateFactory.build(name="Far Courier", location=Location(x=1, y=1))
    courier_near = CourierAggregateFactory.build(name="Near Courier", location=Location(x=4, y=5))

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier_far)
        await uow.couriers.add(courier_near)
        await uow.commit()

    cmd = AssignOrderCommand()
    dispatch_service = DispatchDomainService()
    async with unit_of_work_factory() as uow:
        await assign_order(cmd, uow, dispatch_service)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier_near = await uow.couriers.get_by_id(courier_near.id)
        saved_courier_far = await uow.couriers.get_by_id(courier_far.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatusEnum.ASSIGNED
    assert saved_courier_near is not None
    assert len(saved_courier_near.assignments) == 1
    assert saved_courier_near.assignments[0].order_id == order.id
    assert saved_courier_far is not None
    assert len(saved_courier_far.assignments) == 0
