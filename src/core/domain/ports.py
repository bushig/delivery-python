from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.order import OrderAggregate


class OrderRepository(Protocol):
    async def add(self, order: OrderAggregate) -> None: ...

    async def update(self, order: OrderAggregate) -> None: ...

    async def get_by_id(self, id: UUID) -> OrderAggregate | None: ...

    async def get_any_in_created_status(self) -> OrderAggregate | None: ...

    async def get_all_in_assigned_status(self) -> list[OrderAggregate]: ...

    async def get_all_not_completed(self) -> list[OrderAggregate]: ...


class CourierRepository(Protocol):
    async def add(self, courier: CourierAggregate) -> None: ...

    async def update(self, courier: CourierAggregate) -> None: ...

    async def get_by_id(self, id: UUID) -> CourierAggregate | None: ...

    async def get_all(self) -> list[CourierAggregate]: ...


class UnitOfWork(Protocol):
    orders: OrderRepository
    couriers: CourierRepository

    async def __aenter__(self) -> UnitOfWork: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
