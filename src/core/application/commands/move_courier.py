




from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.location import Location
from src.core.domain.ports import UnitOfWork
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import NotFoundException


@dataclass(frozen=True, slots=True, kw_only=True)
class MoveCourierCommand:
    courier_id: UUID
    location: Location


async def move_courier(cmd: MoveCourierCommand, uow: UnitOfWork) -> None:
    async with uow:
        courier = await uow.couriers.get_by_id(cmd.courier_id)
        if courier is None:
            raise NotFoundException(
                DomainError(code="not_found", message=f"Courier with id={cmd.courier_id} not found"),
            )

        courier.change_location(cmd.location)
        await uow.couriers.update(courier)
        await uow.commit()
