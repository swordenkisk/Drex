# AI Agent Rules (Drex)

This document defines the operating rules for AI coding agents in this Python repository.

## Project Overview

Drex is a Python monorepo for microservices and shared libraries. It uses a modular architecture
with clear domain boundaries. Services communicate via gRPC and event-driven patterns with Kafka.
Shared schemas (e.g., Protobuf, Pydantic models) are defined in dedicated libraries and consumed
by services via generated code or shared helpers.

### Docs Index

See the root [README](README.md) for the full list of service and library docs.

---

## Autonomy Level

- **Medium autonomy**: agents may make small refactors or cleanup changes that stay within the
  existing architecture and folder structure.
- Architecture changes, new services, or cross-domain reorganizations require explicit approval.

---

## Non-Negotiable Guardrails

- Do not invent requirements, domain rules, or data contracts. If anything is unclear, ask first.
- Do not add or change dependencies without explicit approval (`pyproject.toml` / `requirements.txt`
  changes must be approved).
- Do not move or rename folders or change project structure without approval.
- Respect domain boundaries. Do not mix bounded contexts or share logic across domains unless
  explicitly requested.
- Keep changes minimal and localized to the task.

---

## Monorepo Structure

The repository is organized as a monorepo with multiple Python packages (Poetry workspace).

| Path | Role |
|---|---|
| `libs/schema/` | Single source of truth for data contracts (Pydantic models, Protobuf defs) |
| `libs/util/` | Shared helpers: Kafka wrappers, gRPC clients, config loader |
| `libs/feature/` | Reusable business logic — no transport, DB, or app wiring |
| `services/` | Individual microservice applications (each owns `pyproject.toml`, entry point, Dockerfile) |
| `gateway/` | API Gateway — routing and aggregation only |

- All packages are importable via `drex.<package>` namespace.
- Do not create circular dependencies between packages.

---

## Event Sourcing + Kafka Rules

- Events are immutable facts; past events must never be edited.
- Event schemas are defined in `libs/schema` and validated per service (Pydantic or Avro).
- Event versioning is required for any breaking changes (use a schema registry).
- Never publish or consume events from another domain without an explicit contract.
- Event names must use **PascalCase** — e.g., `OrderPlaced`, `PaymentProcessed`.
- Command handlers must **not** write projection/read-model tables directly.
  - Read-model writes must go through event projections subscribed to domain events.
- Projections must be driven by Kafka consumers (`confluent_kafka`, `faust`, or `aiokafka`).
  - Do not implement in-process projection handlers tied to command execution.

---

## API Gateway Rules

- The Gateway performs routing and aggregation only — no business logic.
- Any change in routes or contracts must update gRPC/Protobuf generation as needed.

---

## Tests and Quality

- Every logic change must include tests, or include an explicit note explaining the omission.
- Use `pytest`. Prefer `pytest-asyncio` for async code.
- Maintain strict type hints; avoid `Any` unless justified.
- Run or propose relevant tests for non-trivial changes.
- Prefer integration tests without API mocks; mock only when the real backend cannot run.
- For service integration tests, **do not mock gRPC calls or Kafka** — run against real service
  instances and real databases (use test containers).
- Do not truncate tables between tests; isolate with unique data, transactions, or temporary schemas.
- Do not mock the database in tests; use the real database with isolated data or transaction rollback.
- Tests must be deterministic and parallel-safe.

---

## Documentation

- All documentation must be in **English**.
- All user-facing strings in web interfaces must use a standard i18n library (`gettext`, `Babel`).
  No raw text in templates.
- Group documentation by **feature** (capability-based), not by function or module.
- Each feature section should follow this order where applicable:
  1. Purpose
  2. Commands (if CLI)
  3. Options
  4. Defaults
  5. Examples (runnable, minimal, happy path first)
- `AGENTS.md` — short project overview + links to service/library docs.
- Root `README.md` — architecture overview, microservices list, links to each service README.
- Each microservice must have its own `README.md` (or `docs/` folder) describing: purpose, routes,
  events, and how to run/test it.
- Libraries that are consumed across services must have brief docs; internal-only libs may omit them.
- Update docs when you change contracts, routes, or public behavior.
- When adding a new environment variable: add it to `.env.example`, `.env.test`, and CI config.

---

## ADRs and Worklog

### Architecture Decision Records

- ADRs live in `docs/adr/` and record significant architectural decisions.
- Use an ADR when a decision changes system structure, protocols, data contracts, or
  cross-service behavior.

### Worklog

- Worklogs live in `docs/worklog/` and capture task context, progress, and next steps.
- Do **not** use worklog files for long-lived feature documentation; use `docs/features/*` for that.
- Worklog content must be in **English** even if the user responds in another language.
- Keep worklogs updated continuously during a task, not only at session end.
- Update the worklog for logic changes, decisions, discussions, code changes, or architecture changes.

#### Worklog Commands

| Command | Meaning |
|---|---|
| `wl` | Start a new worklog |
| `wl <slug>` | Continue an existing worklog (match by filename) |
| `wl done` | Mark the worklog as done and update Next steps |

When a worklog is started, ask only for the goal; infer title, scope, and dependencies from that
input, then generate the file from the template in `docs/worklog/`.

---

*Derived from the Juno AI Agent Rules and adapted for the Drex Python monorepo.*
