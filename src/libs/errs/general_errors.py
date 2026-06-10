from __future__ import annotations

from typing import TypeVar

from .error import DomainError

T = TypeVar("T")


class GeneralErrors:
    @staticmethod
    def not_found(name: str, id_: object) -> DomainError:
        return DomainError(code="record_not_found", message=f"Record not found. Name: {name}, id: {id_}")

    @staticmethod
    def value_is_invalid(name: str, value: object) -> DomainError:
        return DomainError(code="value_is_invalid", message=f"Value '{value}' is invalid for {name}")

    @staticmethod
    def value_is_required(name: str) -> DomainError:
        return DomainError(code="value_is_required", message=f"Value is required for {name}")

    @staticmethod
    def invalid_length(name: str) -> DomainError:
        return DomainError(code="invalid_string_length", message=f"Invalid {name} length")

    @staticmethod
    def collection_is_too_small(min_size: int, current: int) -> DomainError:
        return DomainError(
            code="collection_is_too_small",
            message=f"The collection must contain {min_size} items or more. It contains {current} items.",
        )

    @staticmethod
    def collection_is_too_large(max_size: int, current: int) -> DomainError:
        return DomainError(
            code="collection_is_too_large",
            message=f"The collection must contain {max_size} items or fewer. It contains {current} items.",
        )

    @staticmethod
    def value_is_out_of_range(name: str, value: object, min_val: object, max_val: object) -> DomainError:
        return DomainError(
            code="value_is_out_of_range",
            message=f"Value {value} for {name} is out of range. Min value is {min_val}, max value is {max_val}.",
        )

    @staticmethod
    def value_must_be_greater_than(name: str, value: object, min_val: object) -> DomainError:
        return DomainError(
            code="value_must_be_greater_than",
            message=f"The value of {name} ({value}) must be greater than {min_val}.",
        )

    @staticmethod
    def value_must_be_greater_or_equal(name: str, value: object, min_val: object) -> DomainError:
        return DomainError(
            code="value_must_be_greater_or_equal",
            message=f"The value of {name} ({value}) must be greater than or equal to {min_val}.",
        )

    @staticmethod
    def value_must_be_less_than(name: str, value: object, max_val: object) -> DomainError:
        return DomainError(
            code="value_must_be_less_than",
            message=f"The value of {name} ({value}) must be less than {max_val}.",
        )

    @staticmethod
    def value_must_be_less_or_equal(name: str, value: object, max_val: object) -> DomainError:
        return DomainError(
            code="value_must_be_less_or_equal",
            message=f"The value of {name} ({value}) must be less than or equal to {max_val}.",
        )
