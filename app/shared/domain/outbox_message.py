from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from .value_objects import ValueObject


class OutboxMessage(ValueObject):
    id: UUID
    type: str
    payload: Dict[str, Any]
    occurred_on: datetime
    published_on: Optional[datetime]
