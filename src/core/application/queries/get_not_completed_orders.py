
from uuid import UUID

from src.core.domain.model.location import Location


class NotCompletedOrderResponseDTO:
    id: UUID
    location: Location

def get_not_completed_orders() -> list[NotCompletedOrderResponseDTO]:
    # Получить все заказы из БД в статусах "Created" или "Assigned"

    pass