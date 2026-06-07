from __future__ import annotations

from .base_entity import BaseEntity
from .domain_event import DomainEvent


class Aggregate(BaseEntity):
    _domain_events: list[DomainEvent]

    def __init__(self, id) -> None:
        super().__init__(id)
        self._domain_events: list[DomainEvent] = []

    def get_domain_events(self) -> list[DomainEvent]:
        return list(self._domain_events)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    def raise_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)
