




from uuid import UUID

from src.core.domain.model.location import Location


class MoveCourierCommand:
    courier_id: UUID
    location: Location




def move_courier(cmd: MoveCourierCommand) -> None:
    # Получить курьера из БД
    # Переместить курьера
    # Сохранить все изменения в БД
    pass
