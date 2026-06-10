

from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.assignment import Assignment
from src.core.domain.model.location import Location
from src.core.domain.model.order import Order
from src.core.domain.model.volume import Volume


@dataclass
class CourierAggregate:
    id: UUID
    name: str
    location: Location
    max_volume: Volume = Volume(20)
    assignments: list[Assignment] = []


    def can_take_order(self, new_order: Order) -> bool:
        current_total_volume = sum([i.volume.value for i in self.assignments])
        if current_total_volume + new_order.volume.value > self.max_volume.value:
            return False

        return True

    def take_order(self, new_order: Order) -> None:
        if not self.can_take_order:
            raise ValueError("cant take assignment - too big")

        new_assignment = Assignment.create_from_order(order=new_order)
        self.assignments.append(new_assignment)

    def complete_assignment(self, assignment: Assignment) -> None:
        if assignment not in self.assignments:
            raise ValueError("cant complete assignment - not in assignment list")
        if assignment.location.calculate_distance(self.location) > 1:
            raise ValueError("cant complete assignment - too far away")

        # TODO: find assignment in list and pop it
        assignment.complete_assignment(self.location)

        # TODO: complete order

    def change_location(self, new_location: Location):
        Location.check_is_valid_coordinates(new_location.x, new_location.y)

        self.location = new_location





