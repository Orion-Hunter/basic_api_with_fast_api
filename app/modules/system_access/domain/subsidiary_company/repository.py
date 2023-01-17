from abc import ABC, abstractmethod
from typing import Optional

from result import Result

from app.modules.system_access.domain.subsidiary_company.subsidiary_company import (
    SubsidiaryCompany,
)
from app.shared.domain import UUID


class SubsidiaryCompanyRepo(ABC):
    @abstractmethod
    async def insert(self, subsidiary_company: SubsidiaryCompany) -> None:
        ...

    @abstractmethod
    async def get(
        self, parent_company_id: UUID, subsidiary_company_id: UUID
    ) -> Optional[SubsidiaryCompany]:
        ...

    @abstractmethod
    async def update(self, subsidiary_company: SubsidiaryCompany) -> None:
        ...

    @abstractmethod
    async def delete(
        self, parent_company_id: UUID, subsidiary_company_id: UUID
    ) -> Result[None, None]:
        ...
