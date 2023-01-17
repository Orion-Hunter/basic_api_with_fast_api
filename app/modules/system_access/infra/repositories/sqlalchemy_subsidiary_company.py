from typing import Optional

from result import Err, Ok, Result
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.shared.domain import UUID

from ...domain.subsidiary_company import SubsidiaryCompany, SubsidiaryCompanyRepo
from ...domain.value_objects import Address


class SqlAlchemySubsidiaryCompanyRepo(SubsidiaryCompanyRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def insert(self, subsidiary_company: SubsidiaryCompany) -> None:
        db_subsidiary_company = models.SubsidiaryCompany(
            id=subsidiary_company.id,
            parent_company_id=subsidiary_company.parent_company_id,
            company_name=subsidiary_company.company_name,
            company_cnpj=subsidiary_company.company_cnpj,
            company_phone=subsidiary_company.company_phone,
            city=subsidiary_company.address.city,
            state=subsidiary_company.address.state,
            district=subsidiary_company.address.district,
            number=subsidiary_company.address.number,
        )

        self._session.add(db_subsidiary_company)
        await self._session.flush()

    async def get(
        self, parent_company_id: UUID, subsidiary_company_id: UUID
    ) -> Optional[SubsidiaryCompany]:
        query = (
            select(
                models.SubsidiaryCompany.id,
                models.SubsidiaryCompany.parent_company_id,
                models.SubsidiaryCompany.company_name,
                models.SubsidiaryCompany.company_cnpj,
                models.SubsidiaryCompany.company_phone,
                models.SubsidiaryCompany.city,
                models.SubsidiaryCompany.district,
                models.SubsidiaryCompany.state,
                models.SubsidiaryCompany.number,
            )
            .select_from(models.SubsidiaryCompany)
            .where(
                and_(
                    models.SubsidiaryCompany.parent_company_id
                    == str(parent_company_id),
                    models.SubsidiaryCompany.id == str(subsidiary_company_id),
                )
            )
        )

        result = await self._session.execute(statement=query)
        row = result.one_or_none()
        if not row:
            return None

        return SubsidiaryCompany(
            id=row.id,
            parent_company_id=row.parent_company_id,
            company_name=row.company_name,
            company_cnpj=row.company_cnpj,
            company_phone=row.company_phone,
            address=Address(
                city=row.city, state=row.state, district=row.district, number=row.number
            ),
        )

    async def update(self, subsidiary_company: SubsidiaryCompany) -> None:
        statement = (
            update(models.SubsidiaryCompany)
            .where(
                and_(
                    models.SubsidiaryCompany.parent_company_id
                    == str(subsidiary_company.parent_company_id),
                    models.SubsidiaryCompany.id == str(subsidiary_company.id),
                )
            )
            .values(
                company_name=subsidiary_company.company_name,
                company_cnpj=subsidiary_company.company_cnpj,
                company_phone=subsidiary_company.company_phone,
                city=subsidiary_company.address.city,
                district=subsidiary_company.address.district,
                state=subsidiary_company.address.state,
                number=subsidiary_company.address.number,
            )
        )

        await self._session.execute(statement=statement)
        await self._session.flush()

    async def delete(
        self, parent_company_id: UUID, subsidiary_company_id: UUID
    ) -> Result[None, None]:
        subsidiary_company = delete(models.SubsidiaryCompany).where(
            and_(
                models.SubsidiaryCompany.parent_company_id == str(parent_company_id),
                models.SubsidiaryCompany.id == str(subsidiary_company_id),
            )
        )
        result = await self._session.execute(subsidiary_company)
        if result.rowcount == 0:  # type: ignore
            await self._session.rollback()
            return Err(None)

        await self._session.flush()
        return Ok(None)
