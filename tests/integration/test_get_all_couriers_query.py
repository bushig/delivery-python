from __future__ import annotations

from src.core.application.queries.get_all_couriers import get_all_couriers
from src.core.domain.model.location import Location
from tests.factories import CourierAggregateFactory


async def test_get_all_couriers_returns_all_couriers(unit_of_work_factory) -> None:
    c1 = CourierAggregateFactory.build(name="Alice", location=Location(x=1, y=2))
    c2 = CourierAggregateFactory.build(name="Bob", location=Location(x=3, y=4))

    async with unit_of_work_factory() as uow:
        await uow.couriers.add(c1)
        await uow.couriers.add(c2)
        await uow.commit()

    async with unit_of_work_factory() as uow:
        result = await get_all_couriers(uow)

    assert len(result) == 2

    names = {dto.name for dto in result}
    assert names == {"Alice", "Bob"}

    locations = {(dto.location.x, dto.location.y) for dto in result}
    assert locations == {(1, 2), (3, 4)}


async def test_get_all_couriers_empty(unit_of_work_factory) -> None:
    async with unit_of_work_factory() as uow:
        result = await get_all_couriers(uow)

    assert len(result) == 0
