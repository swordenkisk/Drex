"""
drex.schema.events — Base event contract for all Kafka domain events.
© 2025 swordenkisk — All Rights Reserved.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import ClassVar

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """
    Immutable base class for all Drex domain events.

    Conventions
    -----------
    - Event names must use PascalCase (e.g. OrderPlaced, PaymentProcessed).
    - Subclasses must define `event_type` as a ClassVar[str].
    - Past events must never be mutated; create a new version instead.

    Example
    -------
    .. code-block:: python

        class OrderPlaced(BaseEvent):
            event_type: ClassVar[str] = "OrderPlaced"
            order_id: uuid.UUID
            total_amount: float
    """

    model_config = {"frozen": True}

    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: int = Field(default=1, ge=1)

    # Subclasses must override this.
    event_type: ClassVar[str] = "BaseEvent"

    def to_kafka_value(self) -> bytes:
        """Serialize to UTF-8 JSON bytes for Kafka publishing."""
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_kafka_value(cls, data: bytes) -> "BaseEvent":
        """Deserialize from Kafka message bytes."""
        return cls.model_validate_json(data)
