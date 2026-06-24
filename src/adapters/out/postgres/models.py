from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.out.postgres.database import Base
from src.core.domain.model.assignment import Assignment, AssignmentStatusEnum
from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    location_x: Mapped[int] = mapped_column()
    location_y: Mapped[int] = mapped_column()
    volume: Mapped[Decimal] = mapped_column()
    status: Mapped[str] = mapped_column(String(20))

    def _to_domain(self) -> OrderAggregate:
        return OrderAggregate(
            id=self.id,
            location=Location(x=self.location_x, y=self.location_y),
            volume=Volume(_value=self.volume),
            status=OrderStatusEnum(self.status),
        )

    @classmethod
    def _from_domain(cls, order: OrderAggregate) -> OrderModel:
        return cls(
            id=order.id,
            location_x=order.location.x,
            location_y=order.location.y,
            volume=order.volume._value,
            status=order.status.value,
        )

    def _update_from_domain(self, order: OrderAggregate) -> None:
        self.location_x = order.location.x
        self.location_y = order.location.y
        self.volume = order.volume._value
        self.status = order.status.value


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    courier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("couriers.id"))
    order_id: Mapped[uuid.UUID] = mapped_column()
    volume: Mapped[Decimal] = mapped_column()
    location_x: Mapped[int] = mapped_column()
    location_y: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(20))

    def _to_domain(self) -> Assignment:
        return Assignment(
            id=self.id,
            order_id=self.order_id,
            volume=Volume(_value=self.volume),
            location=Location(x=self.location_x, y=self.location_y),
            status=AssignmentStatusEnum(self.status),
        )

    @classmethod
    def _from_domain(cls, assignment: Assignment, courier_id: uuid.UUID) -> AssignmentModel:
        return cls(
            id=assignment.id,
            courier_id=courier_id,
            order_id=assignment.order_id,
            volume=assignment.volume._value,
            location_x=assignment.location.x,
            location_y=assignment.location.y,
            status=assignment.status.value,
        )

    def _update_from_domain(self, assignment: Assignment) -> None:
        self.order_id = assignment.order_id
        self.volume = assignment.volume._value
        self.location_x = assignment.location.x
        self.location_y = assignment.location.y
        self.status = assignment.status.value


class CourierModel(Base):
    __tablename__ = "couriers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_x: Mapped[int] = mapped_column()
    location_y: Mapped[int] = mapped_column()
    max_volume: Mapped[Decimal] = mapped_column()

    assignments: Mapped[list[AssignmentModel]] = relationship(
        backref="courier",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def _to_domain(self) -> CourierAggregate:
        assignments = [a._to_domain() for a in self.assignments]
        return CourierAggregate(
            id=self.id,
            name=self.name,
            location=Location(x=self.location_x, y=self.location_y),
            max_volume=Volume(_value=self.max_volume),
            assignments=assignments,
        )

    @classmethod
    def _from_domain(cls, courier: CourierAggregate) -> CourierModel:
        model = cls(
            id=courier.id,
            name=courier.name,
            location_x=courier.location.x,
            location_y=courier.location.y,
            max_volume=courier.max_volume._value,
        )
        model.assignments = [
            AssignmentModel._from_domain(a, courier_id=courier.id)
            for a in courier.assignments
        ]
        return model

    def _update_from_domain(self, courier: CourierAggregate) -> None:
        self.name = courier.name
        self.location_x = courier.location.x
        self.location_y = courier.location.y
        self.max_volume = courier.max_volume._value

        domain_assignments = {a.id: a for a in courier.assignments}
        existing_ids = {a.id for a in self.assignments}

        self.assignments = [
            a for a in self.assignments if a.id in domain_assignments
        ]

        for assignment_model in self.assignments:
            domain_assignment = domain_assignments[assignment_model.id]
            assignment_model._update_from_domain(domain_assignment)

        for domain_assignment in courier.assignments:
            if domain_assignment.id not in existing_ids:
                self.assignments.append(
                    AssignmentModel._from_domain(domain_assignment, courier_id=courier.id)
                )
