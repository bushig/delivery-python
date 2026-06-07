from __future__ import annotations

import uuid
from collections.abc import Collection
from typing import TypeVar

from delivery.libs.errs.error import DomainError
from delivery.libs.errs.exceptions import (
    ValueIsOutOfRangeException,
    ValueIsRequiredException,
)

T = TypeVar("T")

_EMPTY_UUID = uuid.UUID(int=0)


class Guard:
    @staticmethod
    def against_null_or_empty(value: str | None, param_name: str) -> None:
        if value is None or not value.strip():
            raise ValueIsRequiredException(DomainError.of("value.is.required", f"Value is required for {param_name}"))

    @staticmethod
    def against_null_or_empty_collection(value: Collection[object] | None, param_name: str) -> None:
        if value is None or len(value) == 0:
            raise ValueIsRequiredException(DomainError.of("value.is.required", f"Value is required for {param_name}"))

    @staticmethod
    def against_null_or_empty_uuid(value: uuid.UUID | None, param_name: str) -> None:
        if value is None or value == _EMPTY_UUID:
            raise ValueIsRequiredException(DomainError.of("value.is.required", f"Value is required for {param_name}"))

    @staticmethod
    def against_greater_than(value: T, max_val: T, param_name: str) -> None:
        if value is None or value > max_val:  # type: ignore[operator]
            raise ValueIsOutOfRangeException(
                DomainError.of(
                    "value.must.be.less.than",
                    f"The value of {param_name} ({value}) must be less than {max_val}.",
                )
            )

    @staticmethod
    def against_greater_or_equal(value: T, max_val: T, param_name: str) -> None:
        if value is None or value >= max_val:  # type: ignore[operator]
            raise ValueIsOutOfRangeException(
                DomainError.of(
                    "value.must.be.less.or.equal",
                    f"The value of {param_name} ({value}) must be less than or equal to {max_val}.",
                )
            )

    @staticmethod
    def against_less_than(value: T, min_val: T, param_name: str) -> None:
        if value is None or value < min_val:  # type: ignore[operator]
            raise ValueIsOutOfRangeException(
                DomainError.of(
                    "value.must.be.greater.than",
                    f"The value of {param_name} ({value}) must be greater than {min_val}.",
                )
            )

    @staticmethod
    def against_less_or_equal(value: T, min_val: T, param_name: str) -> None:
        if value is None or value <= min_val:  # type: ignore[operator]
            raise ValueIsOutOfRangeException(
                DomainError.of(
                    "value.must.be.greater.or.equal",
                    f"The value of {param_name} ({value}) must be greater than or equal to {min_val}.",
                )
            )

    @staticmethod
    def against_out_of_range(value: T, min_val: T, max_val: T, param_name: str) -> None:
        if value is None or value < min_val or value > max_val:  # type: ignore[operator]
            raise ValueIsOutOfRangeException(
                DomainError.of(
                    "value.is.out.of.range",
                    f"Value {value} for {param_name} is out of range. Min value is {min_val}, max value is {max_val}.",
                )
            )
