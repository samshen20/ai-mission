# CLAUDE.md

## Project context
Tiny CLI that summarises synthetic `events.csv` logs. No server, no UI, no
external APIs. Pure data-in → summary-out.

## Conventions
- **Code:** `src/` — Python 3.11, single-file entry point (`src/cli.py`)
- **Tests:** `tests/` — pytest, one test file per source module
- **Data:** `data/` — input CSVs and output summaries; never commit real PII
- **Config:** `.env` at project root for overrides; `.env.example` checked in
- **Lint/format:** ruff for both linting and formatting; `ruff check . && ruff format .` before commit

## Utilities to prefer
- Python 3.11 standard library (`csv`, `argparse`, `datetime`, `collections`, `pathlib`)
- pytest for tests
- ruff for lint + format
- No Pipenv/Poetry unless standard-library usage outgrows a single `requirements.txt`

## Escalation gates
- **Stop before adding dependencies.** Justify any third-party package with a
  one-line comment above the `import`.
- **Synthetic data only.** No real customer records, no production log samples,
  no PII — even in test fixtures.
- **Never overwrite `spec.md` after sign-off without asking.** Once reviewed
  and committed, `spec.md` changes require explicit permission.
