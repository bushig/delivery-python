from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.models import CourierModel
from src.core.domain.model.courier import CourierAggregate
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import NotFoundException


class CourierRepositoryPostgres:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, courier: CourierAggregate) -> None:
        model = CourierModel._from_domain(courier)
        self._session.add(model)

    async def update(self, courier: CourierAggregate) -> None:
        stmt = select(CourierModel).where(CourierModel.id == courier.id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise NotFoundException(DomainError(code="not_found", message=f"Courier with id={courier.id} not found"))
        model._update_from_domain(courier)

    async def get_by_id(self, id: UUID) -> CourierAggregate | None:
        stmt = select(CourierModel).where(CourierModel.id == id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return model._to_domain()

    async def get_all(self) -> list[CourierAggregate]:
        stmt = select(CourierModel)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [m._to_domain() for m in models]
