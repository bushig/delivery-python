from fastapi import FastAPI

from .routers import (
    complete_order,
    create_courier,
    create_order,
    get_couriers,
    get_orders,
    move_courier,
)

app = FastAPI(
    version='1.0.0',
    title='Swagger Delivery',
    description='Отвечает за учет курьеров, диспетчеризацию доставок, доставку',
)

app.include_router(create_order)
app.include_router(complete_order)
app.include_router(move_courier)
app.include_router(get_orders)
app.include_router(create_courier)
app.include_router(get_couriers)
