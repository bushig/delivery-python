from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel

from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import InvalidStatusTransitionError
from src.libs.errs.result import Result


class OrderStatusEnum(StrEnum):
    created = "Created"
    assigned = "Assigned"
    completed = "Completed"


class OrderAggregate(BaseModel):
    id: UUID
    location: Location
    volume: Volume
    status: OrderStatusEnum = OrderStatusEnum.created

    def change_status(self, new_status: OrderStatusEnum) -> Result["OrderAggregate", DomainError]:
        if new_status == OrderStatusEnum.assigned:
            if self.status != OrderStatusEnum.created:
                return Result.failure(InvalidStatusTransitionError(message="Order can be assigned only if it is in status 'Created'"))
            self.status = new_status
            return Result.success(self)
        elif new_status == OrderStatusEnum.completed:
            if self.status != OrderStatusEnum.assigned:
                return Result.failure(InvalidStatusTransitionError(message="Order can be completed only if it is in status 'Assigned'"))
            self.status = new_status
            return Result.success(self)
        else:
            return Result.failure(InvalidStatusTransitionError(message="Cant change to this status"))
