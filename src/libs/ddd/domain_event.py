from __future__ import annotations

import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    occurred_on_utc: datetime = Field(default_factory=lambda: datetime.now(UTC))
