


from dataclasses import dataclass

from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.ports import UnitOfWork


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateCourierCommand:
    name: str


async def create_courier(cmd: CreateCourierCommand, uow: UnitOfWork) -> CourierAggregate:
    async with uow:
        courier = CourierAggregate(
            name=cmd.name,
            location=Location.generate_random(),
        )
        await uow.couriers.add(courier)
        await uow.commit()
        return courier
