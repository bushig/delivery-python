


from uuid import UUID

from src.core.domain.model.address import Address
from src.core.domain.model.volume import Volume


class CreateOrderCommand:
    order_id:  UUID
    address: Address
    volume: Volume




def create_order(cmd: CreateOrderCommand) -> None:
    # Создать заказ
    # Сохранить все изменения в БД

    # В следующих уроках мы будем передавать Address в сервис Geo и получать Location. Но пока у нас нет этой интеграции - используйте рандомную Location для создания заказа.
    pass
