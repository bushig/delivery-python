from that_depends import BaseContainer, Provider

from src.core.domain.services.dispatch_service import DispatchDomainService


class Container(BaseContainer):
    dispatch_domain_service = Provider(DispatchDomainService)


container = Container()
