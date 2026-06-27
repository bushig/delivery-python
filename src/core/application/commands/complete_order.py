


from uuid import UUID


class CompleteOrderCommand:
    courier_id: UUID
    order_id: UUID




def complete_order(cmd: CompleteOrderCommand) -> None:
    # Получить курьера из БД
    # Получить заказ из БД
    # Завершить выполнение Assignment для курьера
    # Пометить заказ как завершенный
    # Сохранить все изменения в БД

    pass
