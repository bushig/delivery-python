
from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.location import Location
from src.core.domain.ports import UnitOfWork


@dataclass(frozen=True, slots=True, kw_only=True)
class CourierResponseDTO:
    id: UUID
    name: str
    location: Location


async def get_all_couriers(uow: UnitOfWork) -> list[CourierResponseDTO]:
    async with uow:
        couriers = await uow.couriers.get_all()

    return [
        CourierResponseDTO(
            id=courier.id,
            name=courier.name,
            location=courier.location,
        )
        for courier in couriers
    ]
