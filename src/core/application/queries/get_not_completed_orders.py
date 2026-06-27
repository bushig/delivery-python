
from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.location import Location
from src.core.domain.ports import UnitOfWork


@dataclass(frozen=True, slots=True, kw_only=True)
class NotCompletedOrderResponseDTO:
    id: UUID
    location: Location


async def get_not_completed_orders(uow: UnitOfWork) -> list[NotCompletedOrderResponseDTO]:
    async with uow:
        orders = await uow.orders.get_all_not_completed()

    return [
        NotCompletedOrderResponseDTO(
            id=order.id,
            location=order.location,
        )
        for order in orders
    ]
