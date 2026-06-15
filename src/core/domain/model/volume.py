from dataclasses import dataclass
from decimal import Decimal

from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import ValueIsInvalidError
from src.libs.errs.result import Result


@dataclass(frozen=True)
class Volume:
    value: Decimal

    @staticmethod
    def create(value: Decimal) -> Result["Volume", DomainError]:
        if value <= 0:
            return Result.failure(ValueIsInvalidError(message="Volume can't be negative or zero"))
        return Result.success(Volume(value=value))
