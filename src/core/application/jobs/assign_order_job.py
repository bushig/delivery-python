import logging

from that_depends import Provide, inject

from src.core.application.commands.assign_order_to_courier import AssignOrderCommand, assign_order
from src.core.domain.ports import UnitOfWork
from src.core.domain.services.dispatch_service import DispatchDomainService
from src.di.container import Container

logger = logging.getLogger(__name__)


@inject
async def assign_order_job(
    uow: UnitOfWork = Provide[Container.unit_of_work],
    dispatch_service: DispatchDomainService = Provide[Container.dispatch_domain_service],
) -> None:
    """Periodic job: assign orders to couriers every 1 second."""
    try:
        cmd = AssignOrderCommand()
        await assign_order(cmd, uow, dispatch_service)
        logger.debug("Assign order job completed")
    except Exception as e:
        logger.exception("Error in assign order job: %s", e)
