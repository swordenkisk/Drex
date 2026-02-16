"""
Tests for example_service domain events.

Integration test conventions (per AGENTS.md):
- Do NOT mock Kafka or gRPC — use real broker via testcontainers.
- Do NOT truncate tables; isolate with unique data or transactions.
- Tests must be deterministic and parallel-safe.
"""

import json
import uuid

import pytest

from example_service.events import ExampleCreated, ExampleDeleted


class TestExampleCreated:
    def test_serialization_round_trip(self) -> None:
        event = ExampleCreated(
            example_id=uuid.uuid4(),
            name="Alice",
            created_by="test-user",
        )
        raw = event.to_kafka_value()
        restored = ExampleCreated.from_kafka_value(raw)

        assert restored.example_id == event.example_id
        assert restored.name == event.name
        assert restored.event_type == "ExampleCreated"

    def test_schema_version_defaults_to_one(self) -> None:
        event = ExampleCreated(
            example_id=uuid.uuid4(),
            name="Bob",
            created_by="test-user",
        )
        assert event.schema_version == 1

    def test_event_is_immutable(self) -> None:
        event = ExampleCreated(
            example_id=uuid.uuid4(),
            name="Carol",
            created_by="test-user",
        )
        with pytest.raises(Exception):  # pydantic frozen model raises ValidationError
            event.name = "Mutated"  # type: ignore[misc]

    def test_kafka_value_is_valid_json(self) -> None:
        event = ExampleCreated(
            example_id=uuid.uuid4(),
            name="Dave",
            created_by="test-user",
        )
        parsed = json.loads(event.to_kafka_value())
        assert parsed["name"] == "Dave"
        assert "event_id" in parsed


class TestExampleDeleted:
    def test_event_type_is_correct(self) -> None:
        event = ExampleDeleted(
            example_id=uuid.uuid4(),
            deleted_by="admin",
        )
        assert event.event_type == "ExampleDeleted"
