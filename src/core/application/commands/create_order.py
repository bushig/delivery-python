from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.address import Address
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate
from src.core.domain.model.volume import Volume
from src.core.domain.ports import UnitOfWork


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateOrderCommand:
    order_id: UUID
    address: Address
    volume: Volume


async def create_order(cmd: CreateOrderCommand, uow: UnitOfWork) -> None:
    async with uow:
        random_location = Location.generate_random()
         # В следующих уроках мы будем передавать Address в сервис Geo и получать Location. Но пока у нас нет этой интеграции - используйте рандомную Location для создания заказа.

        order = OrderAggregate(
            id=cmd.order_id,
            location=random_location,
            volume=cmd.volume
        )

        await uow.orders.add(order)
        await uow.commit()
