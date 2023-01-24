from abc import ABC, abstractmethod
from typing import List

from app.shared.domain.domain_events import DomainEvent
from app.shared.domain.outbox_message import OutboxMessage


class OutboxRepo(ABC):
    @abstractmethod
    async def insert(self, domain_events: List[DomainEvent]) -> None:
        ...

    @abstractmethod
    async def get_not_sended(self) -> List[OutboxMessage]:
        ...

    @abstractmethod
    async def set_as_sended(self, outbox_message: OutboxMessage) -> None:
        ...
