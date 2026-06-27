


from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.libs.errs.error import DomainError
from src.libs.errs.exceptions import InvalidStatusTransitionError
from src.libs.errs.result import Result


class DispatchDomainService:
    def dispatch_order_to_courier(self, order: OrderAggregate, couriers: list[CourierAggregate]) -> Result[CourierAggregate, DomainError]:

        if order.status != OrderStatusEnum.CREATED:
            return Result.failure(InvalidStatusTransitionError(message="Can assign to courier only order in 'created' status"))

        suitable_couriers = [courier for courier in couriers if courier.can_take_order(order)]

        if not suitable_couriers:
            return Result.failure(InvalidStatusTransitionError(message="No suitable couriers to assign"))

        best_courier = min(
            suitable_couriers,
            key=lambda c: c.location.calculate_distance(order.location)
        )

        result = best_courier.take_order(order)
        if result.is_failure():
            return Result.failure(result.get_error())

        result = order.change_status(OrderStatusEnum.ASSIGNED)
        if result.is_failure():
            return Result.failure(result.get_error())

        return Result.success(best_courier)


