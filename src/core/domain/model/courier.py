from dataclasses import dataclass, field
from uuid import UUID

from src.core.domain.model.assignment import Assignment, AssignmentStatusEnum
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import AssignmentCapacityExceededError, AssignmentNotPossibleError
from src.libs.errs.result import Result


@dataclass
class CourierAggregate:
    _id: UUID
    _name: str
    _location: Location
    _max_volume: Volume = field(default_factory=lambda: Volume(value=20))
    _assignments: list[Assignment] = field(default_factory=list)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> Location:
        return self._location

    @property
    def max_volume(self) -> Volume:
        return self._max_volume

    @property
    def assignments(self) -> tuple[Assignment, ...]:
        return tuple(self._assignments)

    def can_take_order(self, new_order: OrderAggregate) -> bool:
        current_total_volume = sum([i.volume.value for i in self._assignments if i.status == AssignmentStatusEnum.assigned])
        if current_total_volume + new_order.volume.value > self._max_volume.value:
            return False

        return True

    def take_order(self, new_order: OrderAggregate) -> Result[None, DomainError]:
        if not self.can_take_order(new_order):
            return Result.failure(AssignmentCapacityExceededError(message="cant take assignment - too big"))

        new_assignment = Assignment.create_from_order(order=new_order)
        self._assignments.append(new_assignment)
        return Result.success(None)

    def complete_assignment(self, assignment: Assignment) -> Result[None, DomainError]:
        if assignment not in self._assignments:
            return Result.failure(AssignmentNotPossibleError(message="cant complete assignment - not in assignment list"))
        if assignment.location.calculate_distance(self._location) > 1:
            return Result.failure(AssignmentNotPossibleError(message="cant complete assignment - too far away"))

        result = assignment.complete_assignment(self._location)
        if result.is_failure():
            return Result.failure(result.get_error())

        return Result.success(None)

    def change_location(self, new_location: Location):
        self._location = new_location
