from typing import Optional

from result import Err, Ok, Result
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.shared.domain import UUID

from ...domain.parent_company import ParentCompany, ParentCompanyRepo
from ...domain.value_objects import Address


class SqlAlachemyParentCompanyRepo(ParentCompanyRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def insert(self, parent_company: ParentCompany) -> None:
        db_parent_company = models.ParentCompany(
            id=parent_company.id,
            parent_name=parent_company.parent_name,
            parent_cnpj=parent_company.parent_cnpj,
            parent_phone=parent_company.parent_phone,
            city=parent_company.address.city,
            state=parent_company.address.state,
            district=parent_company.address.district,
            number=parent_company.address.number,
        )

        self._session.add(db_parent_company)
        await self._session.flush()

    async def get(self, parent_company_id: UUID) -> Optional[ParentCompany]:
        query = (
            select(
                models.ParentCompany.id,
                models.ParentCompany.parent_name,
                models.ParentCompany.parent_cnpj,
                models.ParentCompany.parent_phone,
                models.ParentCompany.city,
                models.ParentCompany.district,
                models.ParentCompany.state,
                models.ParentCompany.number,
            )
            .select_from(models.ParentCompany)
            .where(models.ParentCompany.id == str(parent_company_id))
        )

        result = await self._session.execute(statement=query)
        row = result.one_or_none()
        if not row:
            return None

        return ParentCompany(
            id=row.id,
            parent_name=row.parent_name,
            parent_cnpj=row.parent_cnpj,
            address=Address(
                city=row.city, state=row.state, district=row.district, number=row.number
            ),
            parent_phone=row.parent_phone,
        )

    async def update(self, parent_company: ParentCompany) -> None:
        statement = (
            update(models.ParentCompany)
            .where(models.ParentCompany.id == str(parent_company.id))
            .values(
                parent_name=parent_company.parent_name,
                parent_cnpj=parent_company.parent_cnpj,
                parent_phone=parent_company.parent_phone,
                city=parent_company.address.city,
                district=parent_company.address.district,
                state=parent_company.address.state,
                number=parent_company.address.number,
            )
        )

        await self._session.execute(statement=statement)
        await self._session.flush()

    async def delete(self, parent_company_id: Optional[UUID]) -> Result[None, None]:
        parent_company = delete(models.ParentCompany).where(
            and_(
                models.ParentCompany.id == str(parent_company_id),
            )
        )
        result = await self._session.execute(parent_company)
        if result.rowcount == 0:  # type: ignore
            await self._session.rollback()
            return Err(None)

        await self._session.flush()
        return Ok(None)
