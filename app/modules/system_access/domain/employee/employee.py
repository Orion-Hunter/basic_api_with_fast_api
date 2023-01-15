from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Field

from app.shared.domain.aggregates import AggregateRoot

from ..value_objects import Address


class Employee(AggregateRoot):
    parent_company_id: Optional[UUID]
    name: str
    email: EmailStr
    password: Optional[str]
    cpf: str = Field(min_length=11, max_length=11)
    phone: str
    address: Optional[Address]

    @classmethod
    def create(
        cls,
        parent_company_id: UUID,
        name: str,
        email: EmailStr,
        password: Optional[str],
        phone: str,
        address: Optional[Address],
        cpf: str = Field(min_length=11, max_length=11),
    ) -> "Employee":
        employee = Employee(
            parent_company_id=parent_company_id,
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address,
            cpf=cpf,
        )

        return employee
