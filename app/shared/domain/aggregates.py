from typing import List

from pydantic import Field

from .domain_events import DomainEvent
from .entities import Entity


class AggregateRoot(Entity):

    domain_events: List[DomainEvent] = Field([])

    def _record_domain_event(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
