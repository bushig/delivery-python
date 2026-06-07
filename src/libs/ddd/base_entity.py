from __future__ import annotations

from typing import TypeVar

TId = TypeVar("TId")


class BaseEntity:
    id: TId

    def __init__(self, id: TId) -> None:
        self.id = id

    def _is_transient(self) -> bool:
        return self.id is None

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, BaseEntity):
            return False
        if type(self) is not type(other):
            return False
        if self._is_transient() or other._is_transient():
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, str(self.id)))

    def __lt__(self, other: BaseEntity) -> bool:
        if other is None:
            return False
        if self is other:
            return False
        if self.id is None or other.id is None:
            return False
        return self.id < other.id  # type: ignore[operator]
