from typing import Protocol, TypeVar, Generic

from delivery.libs.ddd.domain_event import DomainEvent


class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

    def __eq__(self, other) -> bool: ...


ID = TypeVar("ID", bound=Comparable)


class AggregateRoot(Protocol, Generic[ID]):
    def get_id(self) -> ID: ...

    def get_domain_events(self) -> list[DomainEvent]: ...

    def clear_domain_events(self) -> None: ...
