from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from src.core.application.commands.create_order import CreateOrderCommand, create_order
from src.core.domain.model.location import MIN_X, MAX_X, MIN_Y, MAX_Y
from src.core.domain.model.order import OrderStatusEnum
from tests.factories import AddressFactory, VolumeFactory


async def test_create_order_persists_order_in_db(unit_of_work_factory) -> None:
    order_id = uuid4()
    address = AddressFactory.build()
    volume = VolumeFactory.build(_value=Decimal("5.0"))

    cmd = CreateOrderCommand(
        order_id=order_id,
        address=address,
        volume=volume,
    )

    async with unit_of_work_factory() as uow:
        await create_order(cmd, uow)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order_id)

    assert saved_order is not None
    assert saved_order.id == order_id
    assert saved_order.volume == volume
    assert saved_order.status == OrderStatusEnum.CREATED


async def test_create_order_generates_valid_location(unit_of_work_factory) -> None:
    order_id = uuid4()
    address = AddressFactory.build()
    volume = VolumeFactory.build()

    cmd = CreateOrderCommand(
        order_id=order_id,
        address=address,
        volume=volume,
    )

    async with unit_of_work_factory() as uow:
        await create_order(cmd, uow)

    async with unit_of_work_factory() as uow:
        saved_order = await uow.orders.get_by_id(order_id)

    assert saved_order is not None
    assert MIN_X <= saved_order.location.x <= MAX_X
    assert MIN_Y <= saved_order.location.y <= MAX_Y
