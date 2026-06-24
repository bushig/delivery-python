from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.courier_repository import CourierRepositoryPostgres
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume
from src.libs.errs.exceptions import NotFoundException


@pytest.fixture
def courier_repo(db_session: AsyncSession) -> CourierRepositoryPostgres:
    return CourierRepositoryPostgres(db_session)


def _make_courier(
    name: str = "Courier",
    location: Location | None = None,
    max_volume: Volume | None = None,
) -> CourierAggregate:
    return CourierAggregate(
        name=name,
        location=location or Location(x=1, y=1),
        max_volume=max_volume or Volume(_value=Decimal("20.0")),
    )


def _make_order(
    location: Location | None = None,
    volume: Volume | None = None,
) -> OrderAggregate:
    return OrderAggregate(
        id=uuid4(),
        location=location or Location(x=2, y=2),
        volume=volume or Volume(_value=Decimal("5.0")),
        status=OrderStatusEnum.CREATED,
    )


async def test_add_and_get_by_id(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = _make_courier()

    await courier_repo.add(courier)
    await db_session.commit()

    result = await courier_repo.get_by_id(courier.id)

    assert result is not None
    assert result.id == courier.id
    assert result.name == "Courier"
    assert result.location == Location(x=1, y=1)
    assert result.max_volume == Volume(_value=Decimal("20.0"))
    assert result.assignments == ()


async def test_get_by_id_not_found(courier_repo: CourierRepositoryPostgres) -> None:
    result = await courier_repo.get_by_id(uuid4())

    assert result is None


async def test_get_all(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    c1 = _make_courier(name="Alice")
    c2 = _make_courier(name="Bob")

    await courier_repo.add(c1)
    await courier_repo.add(c2)
    await db_session.commit()

    result = await courier_repo.get_all()

    assert len(result) == 2
    names = {c.name for c in result}
    assert names == {"Alice", "Bob"}


async def test_update(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = _make_courier()
    await courier_repo.add(courier)
    await db_session.commit()

    courier.change_location(Location(x=5, y=5))
    await courier_repo.update(courier)
    await db_session.commit()

    result = await courier_repo.get_by_id(courier.id)
    assert result is not None
    assert result.location == Location(x=5, y=5)


async def test_update_add_assignment(courier_repo: CourierRepositoryPostgres, db_session: AsyncSession) -> None:
    courier = _make_courier()
    order = _make_order()
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
    courier = _make_courier()

    with pytest.raises(NotFoundException):
        await courier_repo.update(courier)
