from .complete_order import router as complete_order
from .create_courier import router as create_courier
from .create_order import router as create_order
from .get_couriers import router as get_couriers
from .get_orders import router as get_orders
from .move_courier import router as move_courier

__all__ = [
    'complete_order',
    'create_courier',
    'create_order',
    'get_couriers',
    'get_orders',
    'move_courier',
]
