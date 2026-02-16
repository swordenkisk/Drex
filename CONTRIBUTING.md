# Contributing to Drex

## ⚠️ License Notice

Drex is **All Rights Reserved**. By submitting a pull request or issue you agree that your
contribution may be incorporated under the same proprietary license.

---

## AI Agents

See [AGENTS.md](AGENTS.md) for the full set of rules governing AI coding agents in this repo.
Agents must read AGENTS.md at the start of every task.

---

## Development Setup

```bash
# Prerequisites: Python 3.11+, Poetry 1.8+, Docker

git clone https://github.com/swordenkisk/drex.git
cd drex

cp .env.example .env          # fill in local values
docker compose up -d          # start Kafka + DB

poetry install                # installs workspace + all packages
```

---

## Code Style

- **Python 3.11+** with strict type hints. Avoid `Any` unless justified.
- Linter/formatter: `ruff` — run `ruff check . && ruff format .` before committing.
- Type checker: `mypy` — run `mypy .` and resolve all errors.

---

## Testing

```bash
pytest                        # all tests
pytest services/example_service/tests/   # single service
pytest -m asyncio             # async-only
```

Rules (from AGENTS.md):
- Do NOT mock Kafka, gRPC, or the database in integration tests.
- Use testcontainers for real infra in CI.
- Do NOT truncate tables between tests; use unique data or transaction rollback.
- Tests must be deterministic and parallel-safe.

---

## Pull Request Checklist

- [ ] Follows existing architecture and folder structure (no new services/folders without approval).
- [ ] No new dependencies added without approval (`pyproject.toml` changes are reviewed).
- [ ] Type hints are complete; `mypy .` passes.
- [ ] `ruff check .` passes with no errors.
- [ ] Tests added or updated; all tests pass.
- [ ] Docs updated if routes, events, or public behavior changed.
- [ ] New env vars added to `.env.example`, `.env.test`, and CI config.
- [ ] ADR created if the change affects system structure, protocols, or data contracts.

---

## Reporting Issues

Open an [Issue](https://github.com/swordenkisk/drex/issues) with:
- A clear title.
- Steps to reproduce (if a bug).
- Expected vs. actual behaviour.
- Python version and OS.
