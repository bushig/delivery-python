from __future__ import annotations

from collections.abc import AsyncIterator

from that_depends import BaseContainer
from that_depends.providers import Factory, Resource

from src.adapters.out.postgres.database import Database
from src.adapters.out.postgres.unit_of_work import UnitOfWorkPostgres
from src.core.domain.services.dispatch_service import DispatchDomainService
from src.settings import settings


async def create_database(url: str) -> AsyncIterator[Database]:
    db = Database(url=url)
    yield db
    await db.dispose()


class Container(BaseContainer):
    database = Resource(create_database, url=settings.db.url)
    unit_of_work = Factory(UnitOfWorkPostgres, database=database.cast)
    dispatch_domain_service = Factory(DispatchDomainService)


container = Container()
