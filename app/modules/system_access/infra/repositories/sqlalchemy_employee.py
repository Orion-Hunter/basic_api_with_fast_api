from typing import Optional

from pydantic import EmailStr
from result import Err, Ok, Result
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.shared.domain import UUID

from ...domain.employee import Employee, EmployeeRepo
from ...domain.value_objects import Address


class SqlAlchemyEmployeeRepo(EmployeeRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def insert(self, employee: Employee) -> None:
        db_employee = models.Employee(
            id=employee.id,
            parent_company_id=employee.parent_company_id,
            name=employee.name,
            email=employee.email,
            password=employee.password,
            cpf=employee.cpf,
            phone=employee.phone,
            city=employee.address.city,
            state=employee.address.state,
            district=employee.address.district,
            number=employee.address.number,
        )

        subsidiaries_transactions_register = None
        if employee.subsidiaries is not None and len(employee.subsidiaries) > 0:
            subsidiaries_transactions_register = [
                models.EmployeeSubsidiaryCompaniesReference(
                    parent_company_id=str(employee.parent_company_id),
                    subsidiary_company_id=str(subsidiary_id),
                    employee_id=str(employee.id),
                )
                for subsidiary_id in employee.subsidiaries
            ]

        self._session.add(db_employee)
        if subsidiaries_transactions_register:
            self._session.add_all(subsidiaries_transactions_register)

        await self._session.flush()

    async def get(
        self, parent_company_id: Optional[UUID], employee_id: UUID
    ) -> Optional[Employee]:
        query = (
            select(
                models.Employee.id,
                models.Employee.parent_company_id,
                models.Employee.name,
                models.Employee.cpf,
                models.Employee.email,
                models.Employee.password,
                models.Employee.phone,
                models.Employee.city,
                models.Employee.district,
                models.Employee.state,
                models.Employee.number,
            )
            .select_from(models.Employee)
            .where(
                and_(
                    models.Employee.parent_company_id == str(parent_company_id),
                    models.Employee.id == str(employee_id),
                )
            )
        )

        query_reference_subsidiary = (
            select(
                models.EmployeeSubsidiaryCompaniesReference.subsidiary_company_id,
            )
            .select_from(models.EmployeeSubsidiaryCompaniesReference)
            .where(
                and_(
                    models.EmployeeSubsidiaryCompaniesReference.parent_company_id
                    == str(parent_company_id),
                    models.EmployeeSubsidiaryCompaniesReference.employee_id
                    == str(employee_id),
                )
            )
        )

        result = await self._session.execute(statement=query)
        row = result.one_or_none()
        if not row:
            return None

        result_subsidiaries = await self._session.execute(query_reference_subsidiary)
        row_subsidiaries = result_subsidiaries.fetchall()

        return Employee(
            id=row.id,
            parent_company_id=row.parent_company_id,
            name=row.name,
            email=row.email,
            password=row.password,
            cpf=row.cpf,
            phone=row.phone,
            address=Address(
                city=row.city, state=row.state, district=row.district, number=row.number
            ),
            subsidiaries=[row_sub.subsidiary_company_id for row_sub in row_subsidiaries]
            if row_subsidiaries is not None
            else None,
        )

    async def get_by_email(
        self, parent_company_id: Optional[UUID], email: EmailStr
    ) -> Optional[Employee]:
        query = (
            select(
                models.Employee.id,
                models.Employee.parent_company_id,
                models.Employee.name,
                models.Employee.cpf,
                models.Employee.email,
                models.Employee.password,
                models.Employee.phone,
                models.Employee.city,
                models.Employee.district,
                models.Employee.state,
                models.Employee.number,
            )
            .select_from(models.Employee)
            .where(
                and_(
                    models.Employee.parent_company_id == str(parent_company_id),
                    models.Employee.email == str(email),
                )
            )
        )

        result = await self._session.execute(statement=query)
        row = result.one_or_none()
        if not row:
            return None

        return Employee(
            id=row.id,
            parent_company_id=row.parent_company_id,
            name=row.name,
            email=row.email,
            password=row.password,
            cpf=row.cpf,
            phone=row.phone,
            address=Address(
                city=row.city, state=row.state, district=row.district, number=row.number
            ),
            subsidiaries=None,
        )

    async def update(self, employee: Employee) -> None:
        statement = (
            update(models.Employee)
            .where(
                and_(
                    models.Employee.parent_company_id
                    == str(employee.parent_company_id),
                    models.Employee.id == str(employee.id),
                )
            )
            .values(
                name=employee.name,
                cpf=employee.cpf,
                email=employee.email,
                password=employee.password,
                phone=employee.phone,
                city=employee.address.city,
                district=employee.address.district,
                state=employee.address.state,
                number=employee.address.number,
            )
        )

        statement_subsidiaries = delete(models.SubsidiaryCompany).where(
            and_(
                models.SubsidiaryCompany.parent_company_id
                == str(employee.parent_company_id),
                models.SubsidiaryCompany.id == str(employee.id),
            )
        )

        subsidiaries_transactions = None
        if employee.subsidiaries is not None and len(employee.subsidiaries) > 0:
            subsidiaries_transactions = [
                models.EmployeeSubsidiaryCompaniesReference(
                    parent_company_id=str(employee.parent_company_id),
                    subsidiary_company_id=str(subsidiary_id),
                    employee_id=str(employee.id),
                )
                for subsidiary_id in employee.subsidiaries
            ]

        await self._session.execute(statement=statement)
        await self._session.execute(statement=statement_subsidiaries)

        if subsidiaries_transactions is not None:
            self._session.add_all(subsidiaries_transactions)

        await self._session.flush()

    async def delete(
        self, parent_company_id: Optional[UUID], employee_id: UUID
    ) -> Result[None, None]:
        employee = delete(models.Employee).where(
            and_(
                models.Employee.parent_company_id == str(parent_company_id),
                models.Employee.id == str(employee_id),
            )
        )
        result = await self._session.execute(employee)
        if result.rowcount == 0:  # type: ignore
            await self._session.rollback()
            return Err(None)

        await self._session.flush()
        return Ok(None)
