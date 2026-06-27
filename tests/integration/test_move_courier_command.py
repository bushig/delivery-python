from __future__ import annotations

from src.core.application.commands.move_courier import MoveCourierCommand, move_courier
from src.core.domain.model.location import Location
from tests.factories import CourierAggregateFactory


async def test_move_courier_updates_location_in_db(unit_of_work_factory) -> None:
    initial_location = Location(x=1, y=1)
    new_location = Location(x=7, y=8)

    courier = CourierAggregateFactory.build(name="Test Courier", location=initial_location)

    async with unit_of_work_factory() as uow:
        await uow.couriers.add(courier)
        await uow.commit()

    cmd = MoveCourierCommand(courier_id=courier.id, location=new_location)

    async with unit_of_work_factory() as uow:
        await move_courier(cmd, uow)

    async with unit_of_work_factory() as uow:
        saved_courier = await uow.couriers.get_by_id(courier.id)

    assert saved_courier is not None
    assert saved_courier.location == new_location


async def test_move_courier_raises_when_courier_not_found(unit_of_work_factory) -> None:
    from uuid import uuid4

    from src.libs.errs.exceptions import NotFoundException

    fake_courier_id = uuid4()
    new_location = Location(x=5, y=5)

    cmd = MoveCourierCommand(courier_id=fake_courier_id, location=new_location)

    async with unit_of_work_factory() as uow:
        try:
            await move_courier(cmd, uow)
            assert False, "Expected NotFoundException"
        except NotFoundException:
            pass
