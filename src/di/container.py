from that_depends import BaseContainer


class Container(BaseContainer):
    """
    DI container placeholder.
    
    Add your own dependencies here as needed.
    Example:
    
    from that_depends import Factory
    from adapters.out.postgres.database import async_session_factory
    from adapters.out.postgres.courier_repository import CourierRepository
    
    @staticmethod
    async def courier_repository(session_factory) -> CourierRepository:
        return CourierRepository(session_factory)
    """

    pass


container = Container()
