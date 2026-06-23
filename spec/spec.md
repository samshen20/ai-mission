# spec.md — events → summary CLI

## 1. Purpose
Read an `events.csv` log file and produce a `summary.csv` with one row per
`(level, service)` group, showing the count and time window of events in that
group.

## 2. Input format
**File:** `data/events.csv` (configurable via `--input`).
**Encoding:** UTF-8.
**Header row required.** Columns, in order:

| Column    | Type   | Example                      |
|-----------|--------|------------------------------|
| timestamp | string | `2026-06-23T14:30:00Z`       |
| level     | string | `ERROR`                      |
| service   | string | `payment-svc`                |
| message   | string | `timeout connecting to gateway` |

Additional columns beyond these four are ignored. Rows with fewer than four
columns are treated as malformed (see §7).

## 3. Group key
Events are grouped by the tuple **`(level, service)`** after normalisation
(see §4). All rows with the same normalised level and normalised service produce
one output row.

## 4. Normalisation
Applied to every input row before grouping:

| Column    | Rule                                                                 |
|-----------|----------------------------------------------------------------------|
| timestamp | Parse as ISO 8601. Normalise to UTC, format `YYYY-MM-DDTHH:MM:SSZ`.  |
| level     | Uppercase, strip whitespace. Map to canonical set: `DEBUG`, `INFO`, `WARN`, `ERROR`. Anything not in the canonical set → `OTHER`. |
| service   | Lowercase, strip whitespace.                                         |
| message   | Strip leading and trailing whitespace only.                          |

## 5. Output format
**File:** `data/summary.csv` (configurable via `--output`).
**Encoding:** UTF-8.
**Header row is written.** Columns, in order:

| Column      | Type    | Description                                   |
|-------------|---------|-----------------------------------------------|
| level       | string  | Normalised level                              |
| service     | string  | Normalised service name                       |
| count       | integer | Number of events in this group                |
| first_seen  | string  | Earliest normalised timestamp in this group   |
| last_seen   | string  | Latest normalised timestamp in this group     |

Rows are written in arbitrary order (no sorting guarantee).

## 6. Missing values

| Column    | Behaviour if missing/empty                                   |
|-----------|--------------------------------------------------------------|
| timestamp | Treat as malformed — skip row, warn to stderr (see §7).      |
| level     | Treat as empty string → normalises to `OTHER`.               |
| service   | Treat as empty string → normalises to empty string.          |
| message   | Treat as empty string → normalises to empty string.          |

## 7. Malformed input
A row is malformed if:
- It has fewer than 4 columns (after CSV parsing).
- Its `timestamp` field is missing, empty, or unparseable as ISO 8601.

Malformed rows are **skipped**. For each skipped row, emit one warning to stderr
with the 1-based line number and reason. At the end of processing, emit a
summary line to stderr: `Skipped N row(s) due to malformed data.`

If **all** rows are malformed, exit code 2, and `summary.csv` contains only the
header row.

## 8. Empty input
If the input file exists but contains only the header row (no data rows):
- Exit code 0.
- Produce `summary.csv` with the header row only.

## 9. CLI interface

```
usage: cli.py [-h] [--version] [--input PATH] [--output PATH]

Summarise events.csv into summary.csv grouped by (level, service).

options:
  -h, --help      show this help message and exit
  --version       show program's version number and exit
  --input PATH    input CSV file (default: data/events.csv)
  --output PATH   output CSV file (default: data/summary.csv)
```

**Exit codes:**

| Code | Meaning                                                          |
|------|------------------------------------------------------------------|
| 0    | Success: output written, no data errors. Includes empty input.   |
| 1    | Usage error: bad flag, input file not found, output directory not writable. |
| 2    | Data errors: one or more rows skipped due to malformed data, but output still produced. |

## 10. Out of scope
- Streaming or real-time input (static file only).
- Multi-file merge or directory scan.
- JSON, Parquet, or any non-CSV output format.
- Config file or environment-variable overrides (flags only).
- Aggregation beyond `(level, service)` — no sub-groups, top-N, percentiles, or
  histograms.
- Sorting guarantee on output rows.
- Network access, database storage, external API calls.
- Message deduplication or pattern-matching (e.g. collapsing UUIDs, stack
  traces, or parameterised values).

## 11. Examples

### 11.1 Basic run

**Input (`data/events.csv`):**
```csv
timestamp,level,service,message
2026-06-23T14:30:00Z,ERROR,payment-svc,timeout connecting to gateway
2026-06-23T14:30:05Z,ERROR,payment-svc,timeout connecting to gateway
2026-06-23T14:31:00Z,INFO,payment-svc,gateway recovered
2026-06-23T15:00:00Z,warn,auth-svc,token near expiry
```

**Output (`data/summary.csv`):**
```csv
level,service,count,first_seen,last_seen
ERROR,payment-svc,2,2026-06-23T14:30:00Z,2026-06-23T14:30:05Z
INFO,payment-svc,1,2026-06-23T14:31:00Z,2026-06-23T14:31:00Z
WARN,auth-svc,1,2026-06-23T15:00:00Z,2026-06-23T15:00:00Z
```

### 11.2 Normalisation edge cases

**Input:**
```csv
timestamp,level,service,message
2026-06-23T12:00:00Z,  error  ,  PAYMENT-SVC  ,  timeout
2026-06-23T12:01:00+02:00,Error,Payment-Svc,timeout
2026-06-23T12:02:00Z,critical,payment-svc,disk full
2026-06-23T12:03:00Z,,payment-svc,   no level field
```

**Output:**
```csv
level,service,count,first_seen,last_seen
ERROR,payment-svc,2,2026-06-23T12:00:00Z,2026-06-23T10:01:00Z
OTHER,payment-svc,2,2026-06-23T12:02:00Z,2026-06-23T12:03:00Z
```

- Rows 1–2: different capitalisation/spacing in `level` and `service` collapse
  into one `(ERROR, payment-svc)` group. Timestamp with `+02:00` offset
  normalises to UTC (`10:01:00Z`).
- Row 3: `critical` is not in the canonical set → `OTHER`.
- Row 4: empty level → `OTHER`.

### 11.3 Malformed rows

**Input:**
```csv
timestamp,level,service,message
not-a-date,ERROR,svc,bad timestamp
2026-06-23T12:00:00Z,INFO        ← only 3 columns
```

**stderr:**
```
Line 2: skipped — unparseable timestamp "not-a-date"
Line 3: skipped — expected 4 columns, got 3
Skipped 2 row(s) due to malformed data.
```

**Output (`data/summary.csv`):**
```csv
level,service,count,first_seen,last_seen
```

Exit code 2.
