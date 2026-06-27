from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import InvalidStatusTransitionError
from src.libs.errs.result import Result


class OrderStatusEnum(StrEnum):
    CREATED = "Created"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"


@dataclass
class OrderAggregate:
    id: UUID
    location: Location
    volume: Volume
    status: OrderStatusEnum = OrderStatusEnum.CREATED

    def change_status(self, new_status: OrderStatusEnum) -> Result[None, DomainError]:
        if new_status == OrderStatusEnum.ASSIGNED:
            if self.status != OrderStatusEnum.CREATED:
                return Result.failure(InvalidStatusTransitionError(message="Order can be assigned only if it is in status 'Created'"))
            self.status = new_status
            return Result.success(None)
        elif new_status == OrderStatusEnum.COMPLETED:
            if self.status != OrderStatusEnum.ASSIGNED:
                return Result.failure(InvalidStatusTransitionError(message="Order can be completed only if it is in status 'Assigned'"))
            self.status = new_status
            return Result.success(None)
        else:
            return Result.failure(InvalidStatusTransitionError(message="Cant change to this status"))
