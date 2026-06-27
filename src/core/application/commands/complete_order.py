


from dataclasses import dataclass
from uuid import UUID

from src.core.domain.model.order import OrderStatusEnum
from src.core.domain.ports import UnitOfWork
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import DomainInvariantException, NotFoundException


@dataclass(frozen=True, slots=True, kw_only=True)
class CompleteOrderCommand:
    courier_id: UUID
    order_id: UUID


async def complete_order(cmd: CompleteOrderCommand, uow: UnitOfWork) -> None:
    async with uow:
        courier = await uow.couriers.get_by_id(cmd.courier_id)
        if courier is None:
            raise NotFoundException(
                DomainError(code="not_found", message=f"Courier with id={cmd.courier_id} not found"),
            )

        order = await uow.orders.get_by_id(cmd.order_id)
        if order is None:
            raise NotFoundException(
                DomainError(code="not_found", message=f"Order with id={cmd.order_id} not found"),
            )

        assignment = courier.get_assignment_by_order_id(order.id)
        if assignment is None:
            raise DomainInvariantException(
                DomainError(
                    code="assignment_not_found",
                    message=f"Assignment for order {cmd.order_id} not found in courier {cmd.courier_id}",
                ),
            )

        result = courier.complete_assignment(assignment.id)
        result.get_value_or_throw()

        result = order.change_status(OrderStatusEnum.COMPLETED)
        result.get_value_or_throw()

        await uow.couriers.update(courier)
        await uow.orders.update(order)
        await uow.commit()
