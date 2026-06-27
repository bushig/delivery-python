from __future__ import annotations

from .error import DomainError


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


class ValueIsRequiredError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="value_is_required", message=message)


class ValueIsInvalidError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="value_is_invalid", message=message)


class ValueIsOutOfRangeError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="value_is_out_of_range", message=message)


class InvalidStatusTransitionError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="invalid_status_transition", message=message)


class AssignmentCapacityExceededError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="assignment_capacity_exceeded", message=message)


class AssignmentNotPossibleError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="assignment_not_possible", message=message)


class OrderAlreadyExistsError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(code="order_already_exists", message=message)
