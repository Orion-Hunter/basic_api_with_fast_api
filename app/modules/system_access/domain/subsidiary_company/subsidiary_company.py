from typing import Optional

from pydantic import Field

from app.shared.domain import UUID
from app.shared.domain.aggregates import AggregateRoot

from ..value_objects import Address


class SubsidiaryCompany(AggregateRoot):
    parent_company_id: UUID
    company_name: str
    company_cnpj: str = Field(min_length=14, max_length=14)
    address: Address
    company_phone: str

    @classmethod
    def create(
        cls,
        parent_company_id: UUID,
        company_name: str,
        company_phone: str,
        address: Address,
        company_cnpj: str = Field(min_length=14, max_length=14),
    ) -> "SubsidiaryCompany":

        subsidiary_company = SubsidiaryCompany(
            parent_company_id=parent_company_id,
            company_name=company_name,
            company_phone=company_phone,
            company_cnpj=company_cnpj,
            address=address,
        )

        return subsidiary_company
