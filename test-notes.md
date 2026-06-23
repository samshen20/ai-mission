# Test notes — logsum spec-to-test run

## Isolation method

Tests were written **from `spec/spec.md` only**, without reading `src/logsum.py`.
This ensures the tests validate the spec, not the implementation.  The
implementation is treated as a black box invoked via `subprocess.run` with temp
CSV files created by `tmp_path`.

## Failure analysis

### 1. `test_example_11_2_normalisation` — first_seen / last_seen order

- **Test expected** (from spec §11.2 example):
  `first_seen=2026-06-23T12:00:00Z`, `last_seen=2026-06-23T10:01:00Z`
- **Implementation returned**:
  `first_seen=2026-06-23T10:01:00Z`, `last_seen=2026-06-23T12:00:00Z`

**Decision: spec ambiguity.**

Spec §5 defines `first_seen` as "Earliest normalised timestamp in this group"
and `last_seen` as "Latest normalised timestamp in this group."  The §11.2
example input has two rows:

| Row | Raw timestamp            | UTC-normalised          |
|-----|--------------------------|-------------------------|
| 1   | `2026-06-23T12:00:00Z`   | `2026-06-23T12:00:00Z` |
| 2   | `2026-06-23T12:01:00+02:00` | `2026-06-23T10:01:00Z` |

The +02:00 offset normalises to 10:01 UTC, which is *earlier* than 12:00 UTC.
The spec example lists `first_seen` as 12:00 and `last_seen` as 10:01, which
contradicts the definitions in §5 — it has "earliest" and "latest" swapped.

The **implementation is correct** (earliest = 10:01, latest = 12:00).  The test
was fixed to follow the §5 definitions rather than the erroneous §11.2 numbers,
with a comment citing the discrepancy.  The spec example should be corrected
separately if the user chooses.

## Summary

| # | Test file | Failures | Root cause |
|---|-----------|----------|------------|
| 1 | `test_logsum.py::test_example_11_2_normalisation` | 1 | Spec ambiguity: §5 definitions contradict §11.2 example values |

**33 of 34 tests passed on first run.  1 spec ambiguity found and resolved.**
