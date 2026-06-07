from typing import Generic, TypeVar

from .error import DomainError

T = TypeVar("T")
E = TypeVar("E", bound=DomainError)


class Result(Generic[T, E]):
    def __init__(self, value: T | None, error: E | None) -> None:
        self._value = value
        self._error = error

    @classmethod
    def success(cls, value: T) -> "Result[T, E]":
        return cls(value=value, error=None)

    @classmethod
    def failure(cls, error: E) -> "Result[T, E]":
        return cls(value=None, error=error)

    def is_success(self) -> bool:
        return self._error is None

    def is_failure(self) -> bool:
        return self._error is not None

    def get_value(self) -> T:
        if self.is_failure():
            raise IllegalStateException("Cannot get value from failed result")
        return self._value  # type: ignore

    def get_error(self) -> E:
        if self.is_success():
            raise IllegalStateException("Cannot get error from successful result")
        return self._error  # type: ignore

    def map(self, mapper) -> "Result":
        if self.is_failure():
            return self
        try:
            mapped_value = mapper(self._value)
            return Result.success(mapped_value)
        except Exception as e:
            return Result.failure(DomainError.of("mapping.error", str(e)))

    def flat_map(self, mapper) -> "Result":
        if self.is_failure():
            return self
        return mapper(self._value)

    def on_success(self, callback) -> "Result[T, E]":
        if self.is_success():
            callback(self._value)
        return self

    def on_failure(self, callback) -> "Result[T, E]":
        if self.is_failure():
            callback(self._error)
        return self

    def fold(self, on_success, on_failure):
        if self.is_success():
            return on_success(self._value)
        return on_failure(self._error)

    def map_error(self, mapper) -> "Result":
        if self.is_failure():
            return Result.failure(mapper(self._error))
        return self

    def get_value_or_throw(self) -> T:
        if self.is_failure():
            from .exceptions import DomainInvariantException

            raise DomainInvariantException(self._error)
        return self._value  # type: ignore


class IllegalStateException(Exception):
    pass
