from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import ValueIsInvalidError
from src.libs.errs.result import Result


class Volume(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Decimal

    @staticmethod
    def create(value: Decimal) -> Result["Volume", DomainError]:
        if value <= 0:
            return Result.failure(ValueIsInvalidError(message="Volume can't be negative or zero"))
        return Result.success(Volume(value=value))
