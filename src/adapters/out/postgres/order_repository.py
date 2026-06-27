from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.models import OrderModel
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import DomainInvariantException, NotFoundException, OrderAlreadyExistsError


class OrderRepositoryPostgres:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, order: OrderAggregate) -> None:
        model = OrderModel._from_domain(order)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError as e:
            error = OrderAlreadyExistsError(message=f"Order with id={order.id} already exists")
            raise DomainInvariantException(error) from e

    async def update(self, order: OrderAggregate) -> None:
        stmt = select(OrderModel).where(OrderModel.id == order.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise NotFoundException(DomainError(code="not_found", message=f"Order with id={order.id} not found"))
        model._update_from_domain(order)

    async def get_by_id(self, id: UUID) -> OrderAggregate | None:
        stmt = select(OrderModel).where(OrderModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return model._to_domain()

    async def get_any_in_created_status(self) -> OrderAggregate | None:
        stmt = select(OrderModel).where(OrderModel.status == OrderStatusEnum.CREATED).limit(1)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return model._to_domain()

    async def get_all_in_assigned_status(self) -> list[OrderAggregate]:
        stmt = select(OrderModel).where(OrderModel.status == OrderStatusEnum.ASSIGNED)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [m._to_domain() for m in models]

    async def get_all_not_completed(self) -> list[OrderAggregate]:
        stmt = select(OrderModel).where(
            OrderModel.status.in_([OrderStatusEnum.CREATED, OrderStatusEnum.ASSIGNED])
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [m._to_domain() for m in models]
