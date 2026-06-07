from __future__ import annotations

from typing import Any


class ValueObject:
    def equality_components(self) -> tuple[Any, ...]:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, ValueObject):
            return False
        return self.equality_components() == other.equality_components()

    def __hash__(self) -> int:
        return hash(self.equality_components())

    def __repr__(self) -> str:
        components = self.equality_components()
        parts = ", ".join(str(c) for c in components)
        return f"{self.__class__.__name__}[{parts}]"
