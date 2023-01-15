from pydantic import Field

from app.shared.domain.value_objects import ValueObject


class Address(ValueObject):
    city: str
    state: str = Field(min_length=2, max_length=2)
    district: str
    number: int
