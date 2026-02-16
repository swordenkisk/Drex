"""
example_service.events — Domain events published by example_service.

Naming convention: PascalCase (e.g. ExampleCreated, ExampleDeleted).
All events inherit from drex.schema.BaseEvent and are immutable.
"""

from __future__ import annotations

import uuid
from typing import ClassVar

from drex.schema.events import BaseEvent


class ExampleCreated(BaseEvent):
    """Published when a new example entity is created."""

    event_type: ClassVar[str] = "ExampleCreated"

    example_id: uuid.UUID
    name: str
    created_by: str


class ExampleDeleted(BaseEvent):
    """Published when an example entity is deleted."""

    event_type: ClassVar[str] = "ExampleDeleted"

    example_id: uuid.UUID
    deleted_by: str
