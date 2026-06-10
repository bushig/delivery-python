import uuid
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import AssignmentNotPossibleError, InvalidStatusTransitionError
from src.libs.errs.result import Result


class AssignmentStatusEnum(StrEnum):
    assigned = "Assigned"
    completed = "Completed"


class Assignment(BaseModel):
    order_id: uuid.UUID
    volume: Volume
    location: Location
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: AssignmentStatusEnum = AssignmentStatusEnum.assigned

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, Assignment):
            if value.id == self.id:
                return True
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def complete_assignment(self, courier_location: Location) -> Result["Assignment", DomainError]:
        if self.status == AssignmentStatusEnum.completed:
            return Result.failure(InvalidStatusTransitionError(message="Assignment already completed"))
        if courier_location.calculate_distance(self.location) > 1:
            return Result.failure(AssignmentNotPossibleError(message="Courier has to be in same location as assignment"))

        self.status = AssignmentStatusEnum.completed
        return Result.success(self)

    @staticmethod
    def create_from_order(order: OrderAggregate) -> "Assignment":
        return Assignment(order_id=order.id, volume=order.volume, location=order.location)
