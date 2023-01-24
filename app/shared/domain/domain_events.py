from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    aggregate_type: str
    aggregate_id: UUID
    occurred_on: datetime = Field(default_factory=datetime.now)
