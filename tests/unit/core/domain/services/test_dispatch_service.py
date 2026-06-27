import uuid

import pytest

from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume
from src.core.domain.services.dispatch_service import DispatchDomainService


class TestDispatchOrderToCourier:

    @pytest.fixture
    def dispatch_service(self):
        return DispatchDomainService()

    @pytest.fixture
    def created_order(self):
        return OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=10),
            status=OrderStatusEnum.CREATED
        )

    def test_chooses_nearest_courier_from_multiple_suitable(self, dispatch_service, created_order):
        courier_far = CourierAggregate(
            name="Far Courier",
            location=Location(x=1, y=1),
            max_volume=Volume(_value=20)
        )
        courier_near = CourierAggregate(
            name="Near Courier",
            location=Location(x=4, y=5),
            max_volume=Volume(_value=20)
        )
        courier_middle = CourierAggregate(
            name="Middle Courier",
            location=Location(x=2, y=3),
            max_volume=Volume(_value=20)
        )

        couriers = [courier_far, courier_near, courier_middle]

        result = dispatch_service.dispatch_order_to_courier(created_order, couriers)

        assert result.is_success()
        assert result.get_value() == courier_near

    def test_dispatches_to_single_courier(self, dispatch_service, created_order):
        courier = CourierAggregate(
            name="Solo Courier",
            location=Location(x=3, y=3),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(created_order, [courier])

        assert result.is_success()
        assert result.get_value() == courier

    def test_excludes_overloaded_couriers_from_dispatch(self, dispatch_service, created_order):
        courier_overloaded = CourierAggregate(
            name="Overloaded Courier",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )
        existing_order = OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=15)
        )
        courier_overloaded.take_order(existing_order)

        courier_available = CourierAggregate(
            name="Available Courier",
            location=Location(x=6, y=6),
            max_volume=Volume(_value=20)
        )

        couriers = [courier_overloaded, courier_available]

        result = dispatch_service.dispatch_order_to_courier(created_order, couriers)

        assert result.is_success()
        assert result.get_value() == courier_available

    def test_all_couriers_overloaded_returns_business_error(self, dispatch_service, created_order):
        courier1 = CourierAggregate(
            name="Courier 1",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )
        courier1.take_order(OrderAggregate(id=uuid.uuid4(), location=Location(x=5, y=5), volume=Volume(_value=15)))

        courier2 = CourierAggregate(
            name="Courier 2",
            location=Location(x=6, y=6),
            max_volume=Volume(_value=20)
        )
        courier2.take_order(OrderAggregate(id=uuid.uuid4(), location=Location(x=6, y=6), volume=Volume(_value=18)))

        result = dispatch_service.dispatch_order_to_courier(created_order, [courier1, courier2])

        assert result.is_failure()
        assert result.get_error().message == "No suitable couriers to assign"

    def test_empty_couriers_list_returns_business_error(self, dispatch_service, created_order):
        result = dispatch_service.dispatch_order_to_courier(created_order, [])

        assert result.is_failure()
        assert result.get_error().message == "No suitable couriers to assign"

    def test_order_in_assigned_status_returns_error(self, dispatch_service):
        order = OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=10),
            status=OrderStatusEnum.ASSIGNED
        )
        courier = CourierAggregate(
            name="Courier",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(order, [courier])

        assert result.is_failure()
        assert "Can assign to courier only order in 'created' status" in result.get_error().message

    def test_order_in_completed_status_returns_error(self, dispatch_service):
        order = OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=10),
            status=OrderStatusEnum.COMPLETED
        )
        courier = CourierAggregate(
            name="Courier",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(order, [courier])

        assert result.is_failure()
        assert "Can assign to courier only order in 'created' status" in result.get_error().message

    def test_changes_order_status_to_assigned_on_success(self, dispatch_service, created_order):
        courier = CourierAggregate(
            name="Courier",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(created_order, [courier])

        assert result.is_success()
        assert created_order.status == OrderStatusEnum.ASSIGNED

    def test_courier_receives_assignment_on_success(self, dispatch_service, created_order):
        courier = CourierAggregate(
            name="Courier",
            location=Location(x=5, y=5),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(created_order, [courier])

        assert result.is_success()
        assert len(courier.assignments) == 1
        assert courier.assignments[0].order_id == created_order.id

    def test_nearest_courier_by_manhattan_distance(self, dispatch_service, created_order):
        order_at_5_5 = OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=10)
        )

        courier_at_3_5 = CourierAggregate(
            name="Courier at (3,5)",
            location=Location(x=3, y=5),
            max_volume=Volume(_value=20)
        )
        courier_at_5_8 = CourierAggregate(
            name="Courier at (5,8)",
            location=Location(x=5, y=8),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(order_at_5_5, [courier_at_3_5, courier_at_5_8])

        assert result.is_success()
        assert result.get_value() == courier_at_3_5

    def test_tie_breaking_when_equal_distance(self, dispatch_service, created_order):
        order_at_5_5 = OrderAggregate(
            id=uuid.uuid4(),
            location=Location(x=5, y=5),
            volume=Volume(_value=10)
        )

        courier1 = CourierAggregate(
            name="Courier 1",
            location=Location(x=3, y=5),
            max_volume=Volume(_value=20)
        )
        courier2 = CourierAggregate(
            name="Courier 2",
            location=Location(x=7, y=5),
            max_volume=Volume(_value=20)
        )

        result = dispatch_service.dispatch_order_to_courier(order_at_5_5, [courier1, courier2])

        assert result.is_success()
        assert result.get_value() == courier1
