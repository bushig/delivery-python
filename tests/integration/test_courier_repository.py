from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.courier_repository import CourierRepositoryPostgres
from src.core.domain.model.location import Location
from src.libs.errs.exceptions import NotFoundException
from tests.factories import CourierAggregateFactory, OrderAggregateFactory


@pytest.fixture
def courier_repo(db_session: AsyncSession) -> CourierRepositoryPostgres:
    return CourierRepositoryPostgres(db_session)


async def test_add_and_get_by_id(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = CourierAggregateFactory.build()

    await courier_repo.add(courier)
    await db_session.commit()

    result = await courier_repo.get_by_id(courier.id)

    assert result is not None
    assert result.id == courier.id
    assert result.name == courier.name
    assert result.location == courier.location
    assert result.max_volume == courier.max_volume
    assert result.assignments == ()


async def test_get_by_id_not_found(courier_repo: CourierRepositoryPostgres) -> None:
    result = await courier_repo.get_by_id(uuid4())

    assert result is None


async def test_get_all(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    c1 = CourierAggregateFactory.build(name="Alice")
    c2 = CourierAggregateFactory.build(name="Bob")

    await courier_repo.add(c1)
    await courier_repo.add(c2)
    await db_session.commit()

    result = await courier_repo.get_all()

    assert len(result) == 2
    names = {c.name for c in result}
    assert names == {"Alice", "Bob"}


async def test_update(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = CourierAggregateFactory.build()
    await courier_repo.add(courier)
    await db_session.commit()

    courier.change_location(Location(x=5, y=5))
    await courier_repo.update(courier)
    await db_session.commit()

    result = await courier_repo.get_by_id(courier.id)
    assert result is not None
    assert result.location == Location(x=5, y=5)


async def test_update_add_assignment(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = CourierAggregateFactory.build()
    order = OrderAggregateFactory.build()
    await courier_repo.add(courier)
    await db_session.commit()

    courier.take_order(order)
    await courier_repo.update(courier)
    await db_session.commit()

    result = await courier_repo.get_by_id(courier.id)
    assert result is not None
    assert len(result.assignments) == 1
    assert result.assignments[0].order_id == order.id


async def test_update_not_found(courier_repo: CourierRepositoryPostgres) -> None:
    courier = CourierAggregateFactory.build()

    with pytest.raises(NotFoundException):
        await courier_repo.update(courier)
