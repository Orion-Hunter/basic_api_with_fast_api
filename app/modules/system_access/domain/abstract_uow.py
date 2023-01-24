from abc import ABC, abstractmethod
from typing import Any, List

from app.shared.domain.domain_events import DomainEvent
from app.shared.domain.outbox_repository import OutboxRepo

from .employee import EmployeeRepo
from .parent_company import ParentCompanyRepo
from .subsidiary_company import SubsidiaryCompanyRepo


class AbstractUnitOfWork(ABC):

    employee_repo: EmployeeRepo
    parent_repo: ParentCompanyRepo
    subsidiary_repo: SubsidiaryCompanyRepo
    outbox_repo: OutboxRepo

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._commit()

    def collect_new_events(self) -> List[DomainEvent]:
        events = []
        for employee in self.employee_repo.events_to_send:
            while employee.domain_events:
                events.append(employee.domain_events.pop(0))
        return events

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
