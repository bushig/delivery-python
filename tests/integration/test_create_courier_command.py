from __future__ import annotations

from src.core.application.commands.create_courier import CreateCourierCommand, create_courier
from src.core.domain.model.location import Location


async def test_create_courier_persists_courier_in_db(unit_of_work_factory) -> None:
    cmd = CreateCourierCommand(name="Test Courier")

    async with unit_of_work_factory() as uow:
        await create_courier(cmd, uow)

    async with unit_of_work_factory() as uow:
        all_couriers = await uow.couriers.get_all()

    assert len(all_couriers) == 1
    courier = all_couriers[0]
    assert courier.name == "Test Courier"
    assert isinstance(courier.location, Location )
    assert courier.max_volume._value == 20
    assert len(courier.assignments) == 0


