from typing import Optional

from pydantic import Field

from app.shared.domain.value_objects import ValueObject


class Address(ValueObject):
    city: Optional[str]
    state: Optional[str] = Field(min_length=2, max_length=2)
    district: Optional[str]
    number: Optional[int]
