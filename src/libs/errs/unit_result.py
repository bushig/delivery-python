from typing import Callable

from .error import DomainError


class UnitResult:
    def __init__(self, error: DomainError | None) -> None:
        self._error = error

    @classmethod
    def success(cls) -> "UnitResult":
        return cls(error=None)

    @classmethod
    def failure(cls, error: DomainError) -> "UnitResult":
        return cls(error=error)

    def is_success(self) -> bool:
        return self._error is None

    def is_failure(self) -> bool:
        return self._error is not None

    def get_error(self) -> DomainError:
        if self.is_success():
            raise IllegalStateException("Cannot get error from successful result")
        return self._error  # type: ignore

    def on_success(self, callback: Callable[[], None]) -> "UnitResult":
        if self.is_success():
            callback()
        return self

    def on_failure(self, callback: Callable[[DomainError], None]) -> "UnitResult":
        if self.is_failure():
            callback(self._error)
        return self

    def fold(self, on_success: Callable[[], None], on_failure: Callable[[DomainError], None]):
        if self.is_success():
            return on_success()
        return on_failure(self._error)

    def merge(self, other: "UnitResult") -> "UnitResult":
        if self.is_failure():
            return self
        return other

    @classmethod
    def from_result(cls, result) -> "UnitResult":
        if result.is_success():
            return cls.success()
        return cls.failure(result.get_error())

    def to_result(self):
        from .result import Result

        if self.is_success():
            return Result.success(None)
        return Result.failure(self._error)

    def get_value_or_throw(self) -> None:
        if self.is_failure():
            from .exceptions import DomainInvariantException

            raise DomainInvariantException(self._error)


class IllegalStateException(Exception):
    pass
