# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] — 2025-XX-XX  *(Initial Release)*

### Added
- Monorepo scaffold with Poetry workspace layout
- `libs/schema` — `BaseEvent` (immutable, Pydantic v2), `BaseModel`
- `libs/util` — `KafkaProducer`, `KafkaConsumer`, `Settings` (pydantic-settings)
- `libs/feature` — placeholder for reusable business logic
- `services/example_service` — reference microservice with domain events and tests
- `gateway` — FastAPI API Gateway (routing and aggregation only)
- `AGENTS.md` — AI agent operating rules (medium autonomy)
- ADR and worklog templates in `docs/`
- `docker-compose.yml` — Kafka + Zookeeper for local development
- `.env.example`, `.env.test`

---

## [Planned — 0.2.0]

- CI pipeline (GitHub Actions): lint → typecheck → test with testcontainers
- First real microservice (replace `example_service`)
- Schema registry integration for Kafka event versioning
- gRPC `.proto` definitions + generated stubs

## [Planned — 1.0.0]

- Production Kubernetes manifests
- Observability: OpenTelemetry traces + Prometheus metrics
- Multi-service integration test suite
