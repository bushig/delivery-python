from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.out.postgres.courier_repository import CourierRepositoryPostgres
from src.adapters.out.postgres.database import Database
from src.adapters.out.postgres.order_repository import OrderRepositoryPostgres
from src.core.domain.ports import UnitOfWork as UnitOfWorkProtocol


class UnitOfWorkImpl(UnitOfWorkProtocol):
    def __init__(self, database: Database) -> None:
        self._database = database
        self._session: AsyncSession | None = None
        self.orders: OrderRepositoryPostgres
        self.couriers: CourierRepositoryPostgres

    async def __aenter__(self) -> UnitOfWorkImpl:
        self._session = self._database.session_factory()
        self.orders = OrderRepositoryPostgres(self._session)
        self.couriers = CourierRepositoryPostgres(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        if self._session is not None:
            await self._session.close()

    async def commit(self) -> None:
        if self._session is not None:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session is not None:
            await self._session.rollback()
