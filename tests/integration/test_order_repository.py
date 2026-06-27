from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.order_repository import OrderRepositoryPostgres
from src.core.domain.model.order import OrderStatusEnum
from src.libs.errs.exceptions import NotFoundException
from tests.factories import OrderAggregateFactory


@pytest.fixture
def order_repo(db_session: AsyncSession) -> OrderRepositoryPostgres:
    return OrderRepositoryPostgres(db_session)


async def test_add_and_get_by_id(order_repo: OrderRepositoryPostgres, db_session: AsyncSession) -> None:
    order = OrderAggregateFactory.build()

    await order_repo.add(order)
    await db_session.commit()

    result = await order_repo.get_by_id(order.id)

    assert result is not None
    assert result.id == order.id
    assert result.location == order.location
    assert result.volume == order.volume
    assert result.status == OrderStatusEnum.CREATED


async def test_get_by_id_not_found(order_repo: OrderRepositoryPostgres) -> None:
    result = await order_repo.get_by_id(uuid4())

    assert result is None


async def test_get_any_in_created_status(order_repo: OrderRepositoryPostgres, db_session: AsyncSession) -> None:
    order1 = OrderAggregateFactory.build(status=OrderStatusEnum.CREATED)
    order2 = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED)

    await order_repo.add(order1)
    await order_repo.add(order2)
    await db_session.commit()

    result = await order_repo.get_any_in_created_status()

    assert result is not None
    assert result.status == OrderStatusEnum.CREATED


async def test_get_any_in_created_status_empty(order_repo: OrderRepositoryPostgres, db_session: AsyncSession) -> None:
    order = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED)
    await order_repo.add(order)
    await db_session.commit()

    result = await order_repo.get_any_in_created_status()

    assert result is None


async def test_get_all_in_assigned_status(order_repo: OrderRepositoryPostgres, db_session: AsyncSession) -> None:
    order1 = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED)
    order2 = OrderAggregateFactory.build(status=OrderStatusEnum.ASSIGNED)
    order3 = OrderAggregateFactory.build(status=OrderStatusEnum.CREATED)

    await order_repo.add(order1)
    await order_repo.add(order2)
    await order_repo.add(order3)
    await db_session.commit()

    result = await order_repo.get_all_in_assigned_status()

    assert len(result) == 2
    assert all(o.status == OrderStatusEnum.ASSIGNED for o in result)


async def test_update(order_repo: OrderRepositoryPostgres, db_session: AsyncSession) -> None:
    order = OrderAggregateFactory.build()
    await order_repo.add(order)
    await db_session.commit()

    order.change_status(OrderStatusEnum.ASSIGNED)
    await order_repo.update(order)
    await db_session.commit()

    result = await order_repo.get_by_id(order.id)
    assert result is not None
    assert result.status == OrderStatusEnum.ASSIGNED


async def test_update_not_found(order_repo: OrderRepositoryPostgres) -> None:
    order = OrderAggregateFactory.build()

    with pytest.raises(NotFoundException):
        await order_repo.update(order)
