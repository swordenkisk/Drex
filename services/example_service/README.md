# example_service

Reference scaffold for Drex microservices.

## Purpose

Demonstrates the standard layout for a Drex service: domain events, Kafka consumer,
gRPC server hook, config via `drex.util.Settings`, and integration tests.

## Events Published

| Event | Topic | Description |
|---|---|---|
| `ExampleCreated` | `example-events` | Emitted when a new example entity is created |
| `ExampleDeleted` | `example-events` | Emitted when an example entity is deleted |

## Events Consumed

*(none — extend as required)*

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker list |
| `LOG_LEVEL` | `INFO` | Logging level |
| `SERVICE_NAME` | `drex-service` | Used in traces and logs |

## How to Run

```bash
# From repo root
poetry install
cd services/example_service
poetry run example-service
```

## How to Test

```bash
# Unit tests (no external infra needed)
pytest services/example_service/tests/

# Integration tests (requires Docker for Kafka / DB)
docker compose up -d
pytest services/example_service/tests/ -m integration
```

## gRPC

*(Not yet implemented — add .proto definitions in `services/example_service/proto/`
and generate stubs with `grpc_tools.protoc`.)*
