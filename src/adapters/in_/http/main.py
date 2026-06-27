from fastapi import APIRouter

from .routers import (
    complete_order,
    create_courier,
    create_order,
    get_couriers,
    get_orders,
    move_courier,
)

http_router = APIRouter()

http_router.include_router(create_order)
http_router.include_router(complete_order)
http_router.include_router(move_courier)
http_router.include_router(get_orders)
http_router.include_router(create_courier)
http_router.include_router(get_couriers)
