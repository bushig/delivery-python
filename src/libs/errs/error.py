from __future__ import annotations


class DomainError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)

    @staticmethod
    def of(code: str, message: str) -> DomainError:
        return DomainError(code=code, message=message)

    def serialize(self) -> str:
        return f"{self.code}||{self.message}"

    @staticmethod
    def deserialize(serialized: str) -> DomainError:
        parts = serialized.split("||")
        if len(parts) < 2:
            raise ValueError(f"Invalid error serialization: '{serialized}'")
        return DomainError(code=parts[0], message=parts[1])

    @staticmethod
    def throw_if(error: DomainError | None) -> None:
        if error is not None:
            from .exceptions import DomainInvariantException

            raise DomainInvariantException(error)
