


from src.core.domain.ports import UnitOfWork
from src.core.domain.services.dispatch_service import DispatchDomainService


class AssignOrderCommand:
    pass


async def assign_order(cmd: AssignOrderCommand, uow: UnitOfWork, dispatch_service: DispatchDomainService) -> None:
    async with uow:
        order = await uow.orders.get_any_in_created_status()
        if order is None:
            return

        couriers = await uow.couriers.get_all()

        result = dispatch_service.dispatch_order_to_courier(order, couriers)
        best_courier = result.get_value_or_throw()

        await uow.orders.update(order)
        await uow.couriers.update(best_courier)
        await uow.commit()
