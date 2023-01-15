from abc import ABC, abstractmethod
from typing import Any

from .employee import EmployeeRepo
from .parent_company import ParentCompanyRepo
from .subsidiary_company import SubsidiaryCompanyRepo


class AbstractUnitOfWork(ABC):

    employee_repo: EmployeeRepo
    parent_company: ParentCompanyRepo
    subsidiary_company: SubsidiaryCompanyRepo

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._commit()

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
