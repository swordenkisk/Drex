# Drex

> **Python monorepo for microservices and shared libraries.**  
> Services communicate via gRPC and Kafka. All data contracts live in a single shared schema library.

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Kafka](https://img.shields.io/badge/Kafka-event--driven-black)](https://kafka.apache.org)
[![gRPC](https://img.shields.io/badge/gRPC-transport-blueviolet)](https://grpc.io)

---

## Architecture Overview

```
                    ┌─────────────────┐
  HTTP clients ───▶ │    Gateway      │  routing + aggregation only
                    └────────┬────────┘
                             │ gRPC
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │  Service A  │   │  Service B  │   │  Service C  │
   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
          │                  │                  │
          └──────────────────▼──────────────────┘
                        ┌─────────┐
                        │  Kafka  │  event bus
                        └─────────┘

  Shared: libs/schema  ·  libs/util  ·  libs/feature
```

All services import schemas from `drex.schema` and helpers from `drex.util`.  
No business logic lives in the Gateway. No domain crosses its bounded context.

---

## Repository Layout

```
drex/
├── libs/
│   ├── schema/          # Single source of truth — Pydantic models, Protobuf defs
│   ├── util/            # Infra helpers — Kafka wrappers, gRPC clients, config
│   └── feature/         # Reusable business logic (no transport / DB wiring)
├── services/
│   └── example_service/ # Scaffold for a real microservice
├── gateway/             # API Gateway (routing + aggregation only)
├── docs/
│   ├── adr/             # Architecture Decision Records
│   ├── worklog/         # Task worklogs (per-session)
│   └── features/        # Long-lived feature documentation
├── AGENTS.md            # AI agent operating rules
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── .env.example
├── .env.test
└── pyproject.toml       # Root workspace config (Poetry / Hatch)
```

---

## Microservices

| Service | Purpose | Docs |
|---|---|---|
| `gateway` | HTTP → gRPC routing and aggregation | [gateway/README.md](gateway/README.md) |
| `services/example_service` | Scaffold / reference implementation | [services/example_service/README.md](services/example_service/README.md) |

---

## Shared Libraries

| Library | Purpose |
|---|---|
| `libs/schema` | Pydantic models, Protobuf definitions, event schemas |
| `libs/util` | Kafka producer/consumer wrappers, gRPC client helpers, config loader |
| `libs/feature` | Portable business logic with no side-effects |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/swordenkisk/Drex.git && cd drex

# 2. Copy environment files
cp .env.example .env

# 3. Start infrastructure (Kafka + databases)
docker compose up -d

# 4. Install all packages (from workspace root)
poetry install

# 5. Run a service
cd services/example_service
poetry run python -m example_service
```

---

## Running Tests

```bash
# All tests (real Kafka + DB via test containers)
pytest

# Async tests only
pytest -m asyncio

# A single service
pytest services/example_service/tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for testing conventions.

---

## Documentation Index

- [AGENTS.md](AGENTS.md) — AI agent operating rules
- [docs/adr/](docs/adr/) — Architecture Decision Records
- [docs/features/](docs/features/) — Long-lived feature docs
- [CHANGELOG.md](CHANGELOG.md)

---

**© 2025 [swordenkisk](https://github.com/swordenkisk) — All Rights Reserved**
