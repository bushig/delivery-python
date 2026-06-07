from __future__ import annotations

from delivery.libs.errs.error import DomainError


class DomainInvariantException(Exception):
    def __init__(self, error: DomainError) -> None:
        self.error = error
        super().__init__(f"Domain invariant violated: {error.message}")


class NotFoundException(DomainInvariantException):
    pass


class ValueIsInvalidException(DomainInvariantException):
    pass


class ValueIsRequiredException(DomainInvariantException):
    pass


class ValueIsOutOfRangeException(DomainInvariantException):
    pass
