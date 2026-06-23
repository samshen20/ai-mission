import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CANONICAL_LEVELS = frozenset({"DEBUG", "INFO", "WARN", "ERROR"})


def normalise_timestamp(raw):
    """Parse ISO 8601, return UTC-normalised string or None on failure."""
    raw = raw.strip()
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def normalise_level(raw):
    """Uppercase, strip, map to canonical set; non-canonical → OTHER."""
    level = raw.strip().upper() if raw else ""
    return level if level in CANONICAL_LEVELS else "OTHER"


def normalise_service(raw):
    """Lowercase, strip."""
    return raw.strip().lower() if raw else ""


def _build_parser():
    """Return an ArgumentParser for the logsum CLI."""
    parser = argparse.ArgumentParser(
        description="Summarise events.csv into summary.csv grouped by (level, service)."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/events.csv",
        help="input CSV file (default: data/events.csv)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="data/summary.csv",
        help="output CSV file (default: data/summary.csv)",
    )
    parser.add_argument(
        "--version", action="version", version="logsum 0.1.0"
    )
    return parser


def _read_and_aggregate(input_path):
    """Read events.csv, normalise fields, and aggregate into (level, service) groups.

    Returns (groups: dict, skipped: int).  Fatal errors call sys.exit(1).
    """
    groups = defaultdict(lambda: {"count": 0, "first_seen": None, "last_seen": None})
    skipped = 0

    try:
        with input_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, [])

            if len(header) < 4:
                print(
                    "Error: input file must have at least 4 columns",
                    file=sys.stderr,
                )
                sys.exit(1)

            for line_no, row in enumerate(reader, start=2):
                if len(row) < 4:
                    print(
                        f"Line {line_no}: skipped — expected 4 columns, got {len(row)}",
                        file=sys.stderr,
                    )
                    skipped += 1
                    continue

                raw_ts, raw_level, raw_service = row[0], row[1], row[2]

                ts = normalise_timestamp(raw_ts)
                if ts is None:
                    print(
                        f'Line {line_no}: skipped — unparseable timestamp "{raw_ts}"',
                        file=sys.stderr,
                    )
                    skipped += 1
                    continue

                level = normalise_level(raw_level)
                service = normalise_service(raw_service)

                g = groups[(level, service)]
                g["count"] += 1
                if g["first_seen"] is None or ts < g["first_seen"]:
                    g["first_seen"] = ts
                if g["last_seen"] is None or ts > g["last_seen"]:
                    g["last_seen"] = ts
    except csv.Error as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    return groups, skipped


def _write_summary(output_path, groups):
    """Write the aggregated groups to a CSV file.

    Fatal errors call sys.exit(1).
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["level", "service", "count", "first_seen", "last_seen"])
            for (level, service), g in groups.items():
                writer.writerow(
                    [level, service, g["count"], g["first_seen"], g["last_seen"]]
                )
    except OSError as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = _build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    groups, skipped = _read_and_aggregate(input_path)
    _write_summary(Path(args.output), groups)

    if skipped > 0:
        print(f"Skipped {skipped} row(s) due to malformed data.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
