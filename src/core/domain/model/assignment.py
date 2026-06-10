
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from pydantic import UUID4

from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume


class AssignmentStatusEnum(StrEnum):
    assigned = "Assigned"
    completed = "Completed"

@dataclass(kw_only=True)
class Assignment:
    """
    Assignment to courier
    """

    order_id: UUID4
    volume: Volume
    location: Location
    id: UUID4 = field(default_factory=uuid.uuid4)
    status: AssignmentStatusEnum = AssignmentStatusEnum.assigned

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, Assignment):
            if value.id == self.id:
                return True
        return False

    def complete_assignment(self, courier_location: Location) -> None:
        if self.status == AssignmentStatusEnum.completed:
            raise ValueError("Assignment already completed")
        if courier_location.calculate_distance(self.location) > 1:
            raise ValueError("Courier has to be in same location as assignment")

        self.status = AssignmentStatusEnum.completed

    @staticmethod
    def create_from_order(order: OrderAggregate) -> "Assignment":
        return Assignment(order_id=order.id, volume=order.volume, location=order.location)
