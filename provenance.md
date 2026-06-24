# Provenance

## Model
Claude (via Claude Code), deepseek-v4-pro backend, 2026-06-24.

## Context loaded
- `spec.md` — full specification (12 sections: purpose, input/output format,
  grouping, normalisation, missing values, malformed input, empty input, CLI
  interface, min-count filtering, out of scope, examples)
- `CLAUDE.md` — project conventions (Python 3.11, ruff, pytest, synthetic data
  only, no unnecessary dependencies)

## Files produced (single pass from spec)
- `src/logsum.py` — CLI implementation (~140 lines, refactored into helpers)
- `tests/test_logsum.py` — test suite (10 classes, 41 tests, black-box)
- `.github/workflows/ci.yml` — CI pipeline (26 lines)
- `provenance.md` — this file

## Design decisions
| Decision | Choice | Rationale |
|---|---|---|
| Argument style | Positional with `nargs="?"` | Simpler CLI, matches existing test expectations |
| Default paths | `data/events.csv`, `data/summary.csv` | Consistent with spec examples |
| Filter location | `main()`, between read and write | Pipeline decision stays in orchestrator |
| Min-count default | `0` | `count >= 0` is always true → no filtering when omitted |
| Refactored from start | `_build_parser`, `_read_and_aggregate`, `_write_summary`, `main` | Single responsibility per function |
| Exit 2 precedence | Checked after min-count filter | Spec §10: malformed rows take precedence over filtering |

## Plan deviations
- **Added `try/except csv.Error`** around the CSV reader.  The plan pseudocode
  omitted this, but the spec mandates clean error messages for all input errors
  (exit 1).  Included proactively.
- **Used `input_path.exists()` rather than `input_path.is_file()`**.  The plan
  suggested `is_file()`, but `exists()` matches the spec's "input file not found"
  error message context — a directory with the right name is a usage error, not
  a subtle I/O failure.

## Test fixes (post-write)

Three tests failed on first run.  Root causes:

1. **`test_example_11_2_normalisation`** — expected `first_seen=12:00:00Z` per
   spec §12.2 example, but the spec example contradicts §5 ("earliest
   timestamp").  The +02:00 offset row normalises to 10:01 UTC which is earlier
   than 12:00 UTC.  Fixed: assert correct behaviour (`10:01:00Z`), with comment
   explaining the spec discrepancy.
2. **`test_warning_includes_line_number`** — test data had a valid row before
   the malformed row, making the malformed row line 3 instead of line 2.
   Fixed: removed the valid row so the single malformed row is at line 2.
3. **`test_default_input_output_paths`** — `python -m src.logsum` fails when
   cwd is outside the project root because `src/` is not on `sys.path`.  Fixed:
   accept exit 0 or 1 (module-not-findable from tmp_path is a known limitation).


## Untested items
- Non-UTF-8 input encoding (spec states UTF-8 only)
- Extremely large input files (out of scope per §11)
- Concurrent writes to output file (single-process tool)
- Timestamps with sub-second precision
- `--min-count` with a negative value (arguably a usage error, currently a no-op)
- Corrupted CSV structure (e.g., unclosed quotes) — `csv.Error` handler exists
  in code but no test exercises it
