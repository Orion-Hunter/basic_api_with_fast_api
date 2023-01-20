from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr
from result import Result

from app.shared.domain import UUID

from .employee import Employee


class EmployeeRepo(ABC):
    @abstractmethod
    async def insert(self, employee: Employee) -> None:
        ...

    @abstractmethod
    async def get(
        self, parent_company_id: Optional[UUID], employee_id: UUID
    ) -> Optional[Employee]:
        ...

    @abstractmethod
    async def get_by_email(
        self, parent_company_id: Optional[UUID], email: EmailStr
    ) -> Optional[Employee]:
        ...

    @abstractmethod
    async def update(self, employee: Employee) -> None:
        ...

    @abstractmethod
    async def delete(
        self, parent_company_id: Optional[UUID], employee_id: UUID
    ) -> Result[None, None]:
        ...
