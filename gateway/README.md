# Gateway

HTTP entry point for the Drex platform. Routes requests to downstream microservices via gRPC.

## Purpose

The Gateway performs **routing and aggregation only**. It contains no business logic.
All domain decisions are delegated to the appropriate microservice.

## Routes

| Method | Path | Upstream service |
|---|---|---|
| GET | `/health` | — (gateway liveness) |

*(Extend this table when adding routes.)*

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GRPC_HOST` | `0.0.0.0` | gRPC bind host |
| `GRPC_PORT` | `50051` | gRPC port |
| `LOG_LEVEL` | `INFO` | Logging level |

## How to Run

```bash
cd gateway
poetry install
poetry run drex-gateway
# → http://localhost:8000
```

## How to Test

```bash
pytest gateway/tests/
```

## Adding a New Route

1. Create `gateway/src/gateway/routers/<domain>_router.py`.
2. Mount it in `main.py` with `app.include_router(...)`.
3. Update this README and the root README route table.
4. If the route requires a new gRPC method, update the `.proto` file and regenerate stubs.
