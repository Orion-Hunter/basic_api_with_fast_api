from typing import Optional

from pydantic import Field

from app.shared.domain.aggregates import AggregateRoot

from ..value_objects import Address


class ParentCompany(AggregateRoot):
    parent_name: str
    parent_cnpj: str = Field(min_length=14, max_length=14)
    address: Optional[Address] = Field(default=None)
    phone: str

    @classmethod
    def create(
        cls,
        parent_name: str,
        phone: str,
        parent_cnpj: str = Field(min_length=14, max_length=14),
        address: Optional[Address] = Field(default=None),
    ) -> "ParentCompany":

        parent_company = ParentCompany(
            parent_name=parent_name,
            phone=phone,
            parent_cnpj=parent_cnpj,
            address=address,
        )

        return parent_company
