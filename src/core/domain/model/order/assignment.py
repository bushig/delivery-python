
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from pydantic import UUID4

from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume


class AssignmentStatusEnum(StrEnum):
    assigned = "Assigned"
    completed = "Completed"

@dataclass
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

    def complete(self, courier_location: Location) -> None:
        if courier_location.calculate_distance(self.location) > 1:
            raise ValueError("Courier has to be in same location as assignment")

        if self.status == AssignmentStatusEnum.completed:
            raise ValueError("Assignment already completed")
        self.status = AssignmentStatusEnum.completed

