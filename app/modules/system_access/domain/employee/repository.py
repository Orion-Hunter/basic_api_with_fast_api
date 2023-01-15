from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import EmailStr

from app.shared.domain import UUID

from .employee import Employee


class EmployeeRepo(ABC):
    @abstractmethod
    async def insert(self, employee: Employee) -> None:
        ...

    @abstractmethod
    async def get(self, parent_company_id: Optional[UUID]) -> Optional[List[Employee]]:
        ...

    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> Optional[Employee]:
        ...

    @abstractmethod
    async def update(self, employee: Employee) -> None:
        ...

    @abstractmethod
    async def delete(self, employee_id: UUID) -> None:
        ...
