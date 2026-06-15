import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import AssignmentNotPossibleError, InvalidStatusTransitionError
from src.libs.errs.result import Result


class AssignmentStatusEnum(StrEnum):
    assigned = "Assigned"
    completed = "Completed"


@dataclass(eq=False)
class Assignment:
    _order_id: uuid.UUID
    _volume: Volume
    _location: Location
    _id: uuid.UUID = field(default_factory=uuid.uuid4)
    _status: AssignmentStatusEnum = AssignmentStatusEnum.assigned

    @property
    def order_id(self) -> uuid.UUID:
        return self._order_id

    @property
    def volume(self) -> Volume:
        return self._volume

    @property
    def location(self) -> Location:
        return self._location

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def status(self) -> AssignmentStatusEnum:
        return self._status

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, Assignment):
            if value.id == self.id:
                return True
        return False

    def __hash__(self) -> int:
        return hash(self.id)

    def complete_assignment(self, courier_location: Location) -> Result["Assignment", DomainError]:
        if self._status == AssignmentStatusEnum.completed:
            return Result.failure(InvalidStatusTransitionError(message="Assignment already completed"))
        if courier_location.calculate_distance(self._location) > 1:
            return Result.failure(AssignmentNotPossibleError(message="Courier has to be in same location as assignment"))

        self._status = AssignmentStatusEnum.completed
        return Result.success(self)

    @staticmethod
    def create_from_order(order: OrderAggregate) -> "Assignment":
        return Assignment(_order_id=order.id, _volume=order.volume, _location=order.location)
