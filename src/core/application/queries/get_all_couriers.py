
from uuid import UUID

from src.core.domain.model.location import Location


class CourierResponseDTO:
    id: UUID
    name: str
    location: Location

def get_all_couriers() -> list[CourierResponseDTO]:
    # Получить всех курьеров из БД

    pass