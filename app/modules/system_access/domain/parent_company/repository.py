from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.system_access.domain.parent_company.parent_company import ParentCompany
from app.shared.domain import UUID


class ParentCompanyRepo(ABC):
    @abstractmethod
    async def insert(self, parent_company: ParentCompany) -> None:
        ...

    @abstractmethod
    async def get(
        self, parent_company_id: Optional[List[UUID]]
    ) -> Optional[List[ParentCompany]]:
        ...

    @abstractmethod
    async def update(self, parent_company: ParentCompany) -> None:
        ...

    @abstractmethod
    async def delete(self, parent_company_id: UUID) -> None:
        ...
