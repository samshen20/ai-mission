# Questions

**Files read:** `src/logsum.py`, `tests/test_logsum.py`, `.github/workflows/ci.yml`, `CLAUDE.md`

## Where is the grouping rule?

Each row is grouped by the combination of its normalized level and service. The key is a `(level, service)` tuple. Aggregation happens in `_read_and_aggregate` at `src/logsum.py:103`, where `g = groups[(level, service)]` uses that tuple as the dict key. The `groups` dict is a `defaultdict` created at `src/logsum.py:70`. Each group accumulates a `count`, `first_seen`, and `last_seen` (`src/logsum.py:104-108`).

The normalization functions that produce the key components are:

- `normalise_level()` at `src/logsum.py:27-29` — uppercases, strips, maps non-canonical values to `"OTHER"`
- `normalise_service()` at `src/logsum.py:33-35` — lowercases and strips

There is no subgrouping and no sorting guarantee on output (`spec/spec.md:108`).

## How is missing level handled?

An empty or missing level becomes `"OTHER"`. The normalization function `normalise_level()` at `src/logsum.py:27-29` does:

```python
level = raw.strip().upper() if raw else ""
return level if level in CANONICAL_LEVELS else "OTHER"
```

When the raw level is empty (falsy), `level` is set to `""`. An empty string is not in `CANONICAL_LEVELS` (`{"DEBUG", "INFO", "WARN", "ERROR"}`, defined at `src/logsum.py:8`), so the function returns `"OTHER"`.

This is tested by `TestMissingValues::test_empty_level_becomes_other` at `tests/test_logsum.py:269`.

Note: an empty *timestamp* is treated differently — `normalise_timestamp()` at `src/logsum.py:11-15` returns `None` for empty input, and the `None` check at `src/logsum.py:99-106` causes the row to be skipped. An empty *service* is kept as an empty string (`src/logsum.py:33-35`).

## How do I run tests and CI locally?

**Run tests:**

```bash
python3 -m pytest tests/ -v
```

This runs all 41 tests across 10 test classes. The tests invoke the CLI as a subprocess — no mocking, no imports of the source module.

**Run lint:**

```bash
python3 -m ruff check .
```

Or if ruff is not installed: `pip install ruff && ruff check .`

**Run both (CI equivalent):**

```bash
python3 -m ruff check . && python3 -m pytest tests/ -v
```

The CI workflow is defined at `.github/workflows/ci.yml:1-25`. It runs the same two commands on Python 3.11 with `ubuntu-latest`. It also installs any `requirements.txt` if present (`.github/workflows/ci.yml:20-21`). There are no secrets, no Docker, and no third-party services involved.

**Could not verify:** Whether `ruff` and `pytest` are installed in the user's local Python environment. The `python3` command is available at `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`. If ruff is not installed, run `pip install ruff pytest`.

## Verification

Every file:line citation from the answers above was opened and checked against
the current file contents.  Results:

| Citation | Claim | Actual | Verdict |
|---|---|---|---|
| `src/logsum.py:103` | `g = groups[(level, service)]` | line 111 | **off by +8** — shifted by `--min-count` additions |
| `src/logsum.py:70` | `groups = defaultdict(...)` | line 73 | **off by +3** — same cause |
| `src/logsum.py:104-108` | count / first_seen / last_seen accumulation | lines 112-116 | **off by +8** — same cause |
| `src/logsum.py:27-29` | `normalise_level()` body | lines 27-30 | **off by +1** — function spans one more line |
| `src/logsum.py:33-35` | `normalise_service()` body | lines 33-35 | **correct** |
| `spec/spec.md:108` | no sorting guarantee | line 108 is now `--min-count` bullet; sorting is line 122 | **off by +14** — spec renumbering moved Out of Scope from §10 to §11 |
| `src/logsum.py:8` | `CANONICAL_LEVELS` | line 8 | **correct** |
| `tests/test_logsum.py:269` | `test_empty_level_becomes_other` | class at 269, method at 270 | **off by +1** — citation names the class line, not the method |
| `src/logsum.py:88-92` | empty timestamp → malformed, skipped | lines 88-92 are the column-count check, not timestamp | **wrong rule** — fixed above; correct citations are `src/logsum.py:11-15` and `src/logsum.py:99-106` |
| `.github/workflows/ci.yml:1-25` | entire CI workflow | file is 25 lines | **correct** |
| `.github/workflows/ci.yml:19-21` | requirements.txt install | line 21 contains it; 19 is `run: \|`, 20 is `pip install` | **off by −2** — specific line is 21 |
| `.github/workflows/ci.yml:20-21` | requirements.txt install | line 21 is requirements.txt; 20 is `pip install ruff pytest` | **off by −1** |
| `.github/workflows/ci.yml:19-25` | ruff + pytest commands | ruff at 23, pytest at 25; 19-25 spans install step too | **imprecise** — should be 23 and 25 |

**One answer fixed:** The empty-timestamp citation originally read `src/logsum.py:88-92`
(which is the "expected 4 columns" guard).  Corrected to `src/logsum.py:11-15`
(the `normalise_timestamp` early-return for empty/whitespace input) and
`src/logsum.py:99-106` (the `ts is None` skip inside the read loop).

**Root cause of systematic off-by:** The `--min-count` feature added 6 lines to
`_build_parser()` and 5 lines to `main()` after the grouping answer was written,
shifting all line numbers inside `_read_and_aggregate()` by +6 to +8.
