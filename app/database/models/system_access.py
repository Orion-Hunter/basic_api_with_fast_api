from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from ..base_class import Base


class ParentCompany(Base):
    __tablename__ = "system_access_parent_company"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_name = Column(String(50), nullable=False)
    parent_cnpj = Column(String(14), nullable=False)
    parent_phone = Column(String, nullable=False)
    city = Column(String, nullable=True)
    state = Column(String(2), nullable=True)
    district = Column(String, nullable=True)
    number = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class SubsidiaryCompany(Base):
    __tablename__ = "system_access_subsidiary_company"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_company_id = Column(
        UUID(as_uuid=True), ForeignKey(ParentCompany.id), index=True, nullable=False
    )
    company_name = Column(String(50), nullable=False)
    company_cnpj = Column(String(14), nullable=False)
    city = Column(String, nullable=True)
    state = Column(String(2), nullable=True)
    district = Column(String, nullable=True)
    number = Column(Integer, nullable=True)
    company_phone = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Employee(Base):
    __tablename__ = "system_access_employee"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_company_id = Column(
        UUID(as_uuid=True), ForeignKey(ParentCompany.id), index=True, nullable=False
    )

    name = Column(String(50), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    cpf = Column(String(11), nullable=False)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=True)
    state = Column(String(2), nullable=True)
    district = Column(String, nullable=True)
    number = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class EmployeeSubsidiaryCompaniesReference(Base):
    __tablename__ = "system_access_employee_subsidiary_reference"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_company_id = Column(
        UUID(as_uuid=True), ForeignKey(ParentCompany.id), index=True, nullable=False
    )

    employee_id = Column(
        UUID(as_uuid=True), ForeignKey(Employee.id), index=True, nullable=False
    )
    subsidiary_company_id = Column(
        UUID(as_uuid=True), ForeignKey(SubsidiaryCompany.id), index=True, nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
