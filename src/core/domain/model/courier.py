from uuid import UUID

from pydantic import BaseModel, Field

from src.core.domain.model.assignment import Assignment
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import AssignmentCapacityExceededError, AssignmentNotPossibleError
from src.libs.errs.result import Result


class CourierAggregate(BaseModel):
    id: UUID
    name: str
    location: Location
    max_volume: Volume = Field(default_factory=lambda: Volume(value=20))
    assignments: list[Assignment] = Field(default_factory=list)

    def can_take_order(self, new_order: OrderAggregate) -> bool:
        current_total_volume = sum([i.volume.value for i in self.assignments])
        if current_total_volume + new_order.volume.value > self.max_volume.value:
            return False

        return True

    def take_order(self, new_order: OrderAggregate) -> Result["CourierAggregate", DomainError]:
        if not self.can_take_order(new_order):
            return Result.failure(AssignmentCapacityExceededError(message="cant take assignment - too big"))

        new_assignment = Assignment.create_from_order(order=new_order)
        self.assignments.append(new_assignment)
        return Result.success(self)

    def complete_assignment(self, assignment: Assignment) -> Result["CourierAggregate", DomainError]:
        if assignment not in self.assignments:
            return Result.failure(AssignmentNotPossibleError(message="cant complete assignment - not in assignment list"))
        if assignment.location.calculate_distance(self.location) > 1:
            return Result.failure(AssignmentNotPossibleError(message="cant complete assignment - too far away"))

        result = assignment.complete_assignment(self.location)
        if result.is_failure():
            return Result.failure(result.get_error())

        return Result.success(self)

    def change_location(self, new_location: Location):
        self.location = new_location
