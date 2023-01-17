from abc import ABC, abstractmethod
from typing import Optional

from result import Result

from app.modules.system_access.domain.parent_company.parent_company import ParentCompany
from app.shared.domain import UUID


class ParentCompanyRepo(ABC):
    @abstractmethod
    async def insert(self, parent_company: ParentCompany) -> None:
        ...

    @abstractmethod
    async def get(self, parent_company_id: UUID) -> Optional[ParentCompany]:
        ...

    @abstractmethod
    async def update(self, parent_company: ParentCompany) -> None:
        ...

    @abstractmethod
    async def delete(self, parent_company_id: UUID) -> Result[None, None]:
        ...
