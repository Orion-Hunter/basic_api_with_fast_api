from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from ..base_class import Base


class OutboxMessage(Base):
    __tablename__ = "outbox_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    aggregate_id = Column(UUID(as_uuid=True))
    aggregate_type = Column(String, nullable=False)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    occurred_on = Column(DateTime, nullable=False)
    published_on = Column(DateTime, nullable=True)
