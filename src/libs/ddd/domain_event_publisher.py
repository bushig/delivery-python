from __future__ import annotations

from typing import Protocol, runtime_checkable

from .aggregate import Aggregate


@runtime_checkable
class DomainEventPublisher(Protocol):
    async def publish(self, aggregates: list[Aggregate]) -> None: ...
