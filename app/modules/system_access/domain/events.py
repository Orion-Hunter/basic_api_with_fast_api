from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from app.shared.domain.domain_events import DomainEvent


class EmployeeRegistered(DomainEvent):
    parent_company_id: Optional[UUID]
    email: EmailStr
