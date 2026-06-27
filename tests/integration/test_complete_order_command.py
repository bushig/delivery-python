from __future__ import annotations

from src.core.application.commands.complete_order import CompleteOrderCommand, complete_order
from src.core.domain.model.assignment import AssignmentStatusEnum
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderStatusEnum
from tests.factories import CourierAggregateFactory, OrderAggregateFactory


async def test_complete_order_success(unit_of_work_factory) -> None:
    order_location = Location(x=5, y=5)
    order = OrderAggregateFactory.build(location=order_location, status=OrderStatusEnum.CREATED)

    courier = CourierAggregateFactory.build(name="Test Courier", location=order_location)
    result = courier.take_order(order)
    assert result.is_success()

    order.change_status(OrderStatusEnum.ASSIGNED)

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = CompleteOrderCommand(courier_id=courier.id, order_id=order.id)

    async with unit_of_work_factory() as uow:
        await complete_order(cmd, uow)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order.id)
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_order is not None
    assert saved_order.status == OrderStatusEnum.COMPLETED

    assert saved_courier is not None
    assert len(saved_courier.assignments) == 1
    assert saved_courier.assignments[0].status == AssignmentStatusEnum.COMPLETED


async def test_complete_order_raises_when_courier_not_found(unit_of_work_factory) -> None:
    from uuid import uuid4

    from src.libs.errs.exceptions import NotFoundException

    fake_courier_id = uuid4()
    order = OrderAggregateFactory.build()

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.commit()

    cmd = CompleteOrderCommand(courier_id=fake_courier_id, order_id=order.id)

    async with unit_of_work_factory() as uow:
        try:
            await complete_order(cmd, uow)
            assert False, "Expected NotFoundException"
        except NotFoundException:
            pass


async def test_complete_order_raises_when_order_not_found(unit_of_work_factory) -> None:
    from uuid import uuid4

    from src.libs.errs.exceptions import NotFoundException

    courier = CourierAggregateFactory.build()
    fake_order_id = uuid4()

    async with unit_of_work_factory() as uow:
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = CompleteOrderCommand(courier_id=courier.id, order_id=fake_order_id)

    async with unit_of_work_factory() as uow:
        try:
            await complete_order(cmd, uow)
            assert False, "Expected NotFoundException"
        except NotFoundException:
            pass


async def test_complete_order_raises_when_assignment_not_found(unit_of_work_factory) -> None:
    from src.libs.errs.exceptions import DomainInvariantException

    order = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED)
    courier = CourierAggregateFactory.build(name="Test Courier", location=order.location)

    async with unit_of_work_factory() as uow:
        await uow.orders.add(order)
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = CompleteOrderCommand(courier_id=courier.id, order_id=order.id)

    async with unit_of_work_factory() as uow:
        try:
            await complete_order(cmd, uow)
            assert False, "Expected DomainInvariantException"
        except DomainInvariantException:
            pass
