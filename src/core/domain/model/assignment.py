import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import AssignmentNotPossibleError, InvalidStatusTransitionError
from src.libs.errs.result import Result


class AssignmentStatusEnum(StrEnum):
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"


@dataclass(eq=False, init=False)
class Assignment:
    _order_id: uuid.UUID
    _volume: Volume
    _location: Location
    _id: uuid.UUID = field(default_factory=uuid.uuid4)
    _status: AssignmentStatusEnum = AssignmentStatusEnum.ASSIGNED

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

    def __init__(
        self,
        order_id: uuid.UUID,
        volume: Volume,
        location: Location,
        id: uuid.UUID | None = None,
        status: AssignmentStatusEnum = AssignmentStatusEnum.ASSIGNED,
    ) -> None:
        self._id = id or uuid.uuid4()
        self._order_id = order_id
        self._volume = volume
        self._location = location
        self._status = status

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, Assignment):
            raise NotImplementedError("Comparison with non-Assignment objects is not supported")
        if value.id == self.id:
            return True
        return False
        

    def __hash__(self) -> int:
        return hash(self.id)

    def complete_assignment(self, courier_location: Location) -> Result[None, DomainError]:
        if self._status == AssignmentStatusEnum.COMPLETED:
            return Result.failure(InvalidStatusTransitionError(message="Assignment already completed"))
        if courier_location.calculate_distance(self._location) > 1:
            return Result.failure(AssignmentNotPossibleError(message="Courier has to be nearby assignment"))

        self._status = AssignmentStatusEnum.COMPLETED
        return Result.success(None)
