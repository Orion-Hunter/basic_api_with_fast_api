from typing import Optional

from passlib.context import CryptContext
from pydantic import Field
from result import Err, Ok, Result

from app.shared.domain import UUID
from app.shared.domain.value_objects import ValueObject

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Address(ValueObject):
    city: Optional[str]
    state: Optional[str] = Field(min_length=2, max_length=2)
    district: Optional[str]
    number: Optional[int]


class SubsidiaryInfo(ValueObject):
    parent_company_id: UUID
    subsidiary_company_id: UUID
    parent_name: str
    company_name: str


class InvalidPassword(Exception):
    ...


class EmployeePassword(ValueObject):
    hashed: str

    @classmethod
    def create(cls, password: str) -> Result["EmployeePassword", InvalidPassword]:
        if not password:
            return Err(InvalidPassword("Senha não fornecida"))
        if len(password) < 8:
            return Err(InvalidPassword("Senha necessita de pelo menos 8 caracteres"))
        return Ok(EmployeePassword(hashed=crypto_context.hash(password)))

    def compare(self, password: str) -> bool:
        return bool(crypto_context.verify(password, self.hashed))

    def __str__(self) -> str:
        return str(self.hashed)
