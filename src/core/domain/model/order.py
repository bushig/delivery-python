

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from src.core.domain.model.location import Location
from src.core.domain.model.volume import Volume


class OrderStatusEnum(StrEnum):
    created = "Created"
    assigned = "Assigned"
    completed = "Completed"


@dataclass
class OrderAggregate:
    id: UUID
    location: Location
    volume: Volume
    status: OrderStatusEnum = OrderStatusEnum.created


    def change_status(self, new_status: OrderStatusEnum) -> None:
        if new_status == OrderStatusEnum.assigned:
            if self.status != OrderStatusEnum.created:
                raise ValueError("Order can be assigned only if it is in status 'Created'")
            self.status = new_status
        elif new_status == OrderStatusEnum.completed:
            if self.status != OrderStatusEnum.assigned:
                raise ValueError("Order can be completed only if it is in status 'Assigned'")
            self.status = new_status
        else:
            raise ValueError("Cant change to this status")