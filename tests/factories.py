from __future__ import annotations

import random
from decimal import Decimal
from typing import Any, TypeVar
from uuid import uuid4

from src.core.domain.model.courier import CourierAggregate
from src.core.domain.model.location import MAX_X, MAX_Y, MIN_X, MIN_Y, Location
from src.core.domain.model.order import OrderAggregate, OrderStatusEnum
from src.core.domain.model.volume import Volume

T = TypeVar("T")


class Factory[T]:
    @classmethod
    def build(cls, **overrides: Any) -> T:
        raise NotImplementedError


class LocationFactory(Factory[Location]):
    @classmethod
    def build(cls, **overrides: Any) -> Location:
        x = overrides.get("x", random.randint(MIN_X, MAX_X))
        y = overrides.get("y", random.randint(MIN_Y, MAX_Y))
        return Location(x=x, y=y)


class VolumeFactory(Factory[Volume]):
    @classmethod
    def build(cls, **overrides: Any) -> Volume:
        value = overrides.get("_value", Decimal(random.randint(1, 20)))
        return Volume(_value=value)


class OrderAggregateFactory(Factory[OrderAggregate]):
    @classmethod
    def build(cls, **overrides: Any) -> OrderAggregate:
        id_ = overrides.get("id")
        if id_ is None:
            id_ = uuid4()
        location = overrides.get("location")
        if location is None:
            location = LocationFactory.build()
        volume = overrides.get("volume")
        if volume is None:
            volume = VolumeFactory.build()
        status = overrides.get("status")
        if status is None:
            status = OrderStatusEnum.CREATED
        return OrderAggregate(
            id=id_,
            location=location,
            volume=volume,
            status=status,
        )


class CourierAggregateFactory(Factory[CourierAggregate]):
    @classmethod
    def build(cls, **overrides: Any) -> CourierAggregate:
        name = overrides.get("name")
        if name is None:
            name = "Courier"
        location = overrides.get("location")
        if location is None:
            location = LocationFactory.build()
        id_ = overrides.get("id", None)
        max_volume = overrides.get("max_volume")
        if max_volume is None:
            max_volume = Volume(_value=Decimal("20.0"))
        assignments = overrides.get("assignments", [])
        return CourierAggregate(
            name=name,
            location=location,
            id=id_,
            max_volume=max_volume,
            assignments=assignments,
        )
