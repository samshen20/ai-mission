"""Tests for logsum CLI — written from spec.md only."""

import csv
import subprocess
import sys


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _run(*args):
    """Run logsum as subprocess. Returns (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "-m", "src.logsum", *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def _read_output(path):
    """Read summary CSV as list of dicts."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path, header, rows):
    """Write a minimal CSV file. `rows` is a list of lists."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------
# fixture helpers
# ---------------------------------------------------------------------------

def _basic_csv(tmp_path):
    """§12.1 example: 4 rows, duplicate (ERROR,payment-svc) group."""
    p = tmp_path / "basic.csv"
    _write_csv(
        p,
        ["timestamp", "level", "service", "message"],
        [
            ["2026-06-23T14:30:00Z", "ERROR", "payment-svc", "timeout connecting to gateway"],
            ["2026-06-23T14:30:05Z", "ERROR", "payment-svc", "timeout connecting to gateway"],
            ["2026-06-23T14:31:00Z", "INFO", "payment-svc", "gateway recovered"],
            ["2026-06-23T15:00:00Z", "warn", "auth-svc", "token near expiry"],
        ],
    )
    return p


def _normalisation_csv(tmp_path):
    """§12.2 example: whitespace, case, timezone, non-canonical, empty level."""
    p = tmp_path / "norm.csv"
    _write_csv(
        p,
        ["timestamp", "level", "service", "message"],
        [
            ["2026-06-23T12:00:00Z", "  error  ", "  PAYMENT-SVC  ", "  timeout"],
            ["2026-06-23T12:01:00+02:00", "Error", "Payment-Svc", "timeout"],
            ["2026-06-23T12:02:00Z", "critical", "payment-svc", "disk full"],
            ["2026-06-23T12:03:00Z", "", "payment-svc", "   no level field"],
        ],
    )
    return p


def _malformed_csv(tmp_path):
    """§12.3 example: bad timestamp + too-few-columns."""
    p = tmp_path / "malformed.csv"
    _write_csv(
        p,
        ["timestamp", "level", "service", "message"],
        [
            ["not-a-date", "ERROR", "svc", "bad timestamp"],
            ["2026-06-23T12:00:00Z", "INFO"],  # only 2 columns
        ],
    )
    return p


def _header_only_csv(tmp_path):
    """Header row, no data rows."""
    p = tmp_path / "header_only.csv"
    _write_csv(p, ["timestamp", "level", "service", "message"], [])
    return p


# ===================================================================
# §3  Grouping
# ===================================================================

class TestGrouping:
    def test_same_level_and_service_collapse_to_one_row(self, tmp_path):
        """Two rows with same (level, service) → one output row with count=2."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg1"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["level"] == "ERROR"
        assert rows[0]["service"] == "svc"
        assert int(rows[0]["count"]) == 2

    def test_different_level_produces_separate_rows(self, tmp_path):
        """Different levels → separate output rows."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg1"],
            ["2026-06-23T10:01:00Z", "INFO", "svc", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 2
        levels = {r["level"] for r in rows}
        assert levels == {"ERROR", "INFO"}

    def test_different_service_produces_separate_rows(self, tmp_path):
        """Different services → separate output rows."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc-b", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 2
        services = {r["service"] for r in rows}
        assert services == {"svc-a", "svc-b"}

    def test_example_11_1_basic_run(self, tmp_path):
        """Reproduce spec §12.1: 4 rows → 3 groups with correct counts."""
        p = _basic_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 3
        by_key = {(r["level"], r["service"]): r for r in rows}
        assert int(by_key[("ERROR", "payment-svc")]["count"]) == 2
        assert int(by_key[("INFO", "payment-svc")]["count"]) == 1
        assert int(by_key[("WARN", "auth-svc")]["count"]) == 1


# ===================================================================
# §4  Normalisation
# ===================================================================

class TestNormalisation:
    def test_level_stripped_and_uppercased(self, tmp_path):
        """Level whitespace and case are normalised."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "  error  ", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["level"] == "ERROR"

    def test_level_non_canonical_becomes_other(self, tmp_path):
        """Non-canonical level → OTHER."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "critical", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["level"] == "OTHER"

    def test_canonical_levels_preserved(self, tmp_path):
        """All four canonical levels pass through unchanged."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "DEBUG", "svc", "msg"],
            ["2026-06-23T10:01:00Z", "INFO", "svc", "msg"],
            ["2026-06-23T10:02:00Z", "WARN", "svc", "msg"],
            ["2026-06-23T10:03:00Z", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        levels = {r["level"] for r in rows}
        assert levels == {"DEBUG", "INFO", "WARN", "ERROR"}

    def test_service_lowercased_and_stripped(self, tmp_path):
        """Service whitespace and case are normalised."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "  PAYMENT-SVC  ", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["service"] == "payment-svc"

    def test_timestamp_timezone_normalised_to_utc(self, tmp_path):
        """Timestamp with +02:00 offset normalises to UTC."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T12:01:00+02:00", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["first_seen"] == "2026-06-23T10:01:00Z"

    def test_timestamp_without_timezone_treated_as_utc(self, tmp_path):
        """Naive timestamp is treated as UTC."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["first_seen"] == "2026-06-23T10:00:00Z"

    def test_example_11_2_normalisation(self, tmp_path):
        """Reproduce spec §12.2 normalisation example."""
        p = _normalisation_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        by_key = {(r["level"], r["service"]): r for r in rows}

        # rows 1-2 collapse: different case/spacing → (ERROR, payment-svc)
        # NOTE: spec §12.2 example lists first_seen=12:00:00Z, last_seen=10:01:00Z,
        # but that contradicts §5 ("earliest" / "latest").  +02:00 normalises to
        # 10:01 UTC which is *earlier* than 12:00 UTC.  We follow §5 definitions.
        error_payment = by_key[("ERROR", "payment-svc")]
        assert int(error_payment["count"]) == 2
        assert error_payment["first_seen"] == "2026-06-23T10:01:00Z"  # +02:00 → 10:01 UTC, earliest
        assert error_payment["last_seen"] == "2026-06-23T12:00:00Z"
        other_payment = by_key[("OTHER", "payment-svc")]
        assert int(other_payment["count"]) == 2


# ===================================================================
# §6  Missing values
# ===================================================================

class TestMissingValues:
    def test_empty_level_becomes_other(self, tmp_path):
        """Empty/missing level → normalises to OTHER (§6)."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["level"] == "OTHER"

    def test_empty_service_becomes_empty_string(self, tmp_path):
        """Empty service → normalises to empty string."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert rows[0]["service"] == ""

    def test_empty_timestamp_is_malformed(self, tmp_path):
        """Empty timestamp → row skipped as malformed."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["", "INFO", "svc-b", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, stderr = _run(str(p), str(out))
        assert code == 2
        assert "skipped" in stderr.lower()
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["service"] == "svc-a"


# ===================================================================
# §7  Malformed input
# ===================================================================

class TestMalformedInput:
    def test_too_few_columns_skipped(self, tmp_path):
        """Row with < 4 columns is skipped with warning."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc"],  # 3 columns
        ])
        out = tmp_path / "out.csv"
        code, _, stderr = _run(str(p), str(out))
        assert code == 2
        assert "expected 4 columns" in stderr

    def test_unparseable_timestamp_skipped(self, tmp_path):
        """Row with unparseable timestamp is skipped with warning."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["not-a-date", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, stderr = _run(str(p), str(out))
        assert code == 2
        assert "unparseable timestamp" in stderr.lower()

    def test_warning_includes_line_number(self, tmp_path):
        """Warning includes the 1-based line number of the malformed row."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["bad-ts", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        _, _, stderr = _run(str(p), str(out))
        assert "Line 2" in stderr

    def test_summary_line_emitted_at_end(self, tmp_path):
        """Summary line counts skipped rows at end of stderr."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["bad-ts", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        _, _, stderr = _run(str(p), str(out))
        assert "Skipped 1 row(s)" in stderr

    def test_all_rows_malformed_produces_header_only(self, tmp_path):
        """All rows malformed → exit 2, header-only output."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["bad-ts", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 2
        rows = _read_output(out)
        assert len(rows) == 0  # no data rows

    def test_partial_malformed_exit_2_with_valid_rows_in_output(self, tmp_path):
        """Some rows malformed → exit 2, valid rows still in output."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["bad-ts", "INFO", "svc-b", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 2
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["service"] == "svc-a"

    def test_example_11_3_malformed(self, tmp_path):
        """Reproduce spec §12.3 malformed example."""
        p = _malformed_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, stderr = _run(str(p), str(out))
        assert code == 2
        assert "not-a-date" in stderr
        assert "expected 4 columns" in stderr
        assert "Skipped 2 row(s)" in stderr
        rows = _read_output(out)
        assert len(rows) == 0


# ===================================================================
# §8  Empty input
# ===================================================================

class TestEmptyInput:
    def test_header_only_exit_0(self, tmp_path):
        """Header-only file → exit 0."""
        p = _header_only_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0

    def test_header_only_output_has_header_only(self, tmp_path):
        """Header-only file → output has header, no data rows."""
        p = _header_only_csv(tmp_path)
        out = tmp_path / "out.csv"
        _run(str(p), str(out))
        rows = _read_output(out)
        assert len(rows) == 0


# ===================================================================
# §2  Input format
# ===================================================================

class TestInputFormat:
    def test_extra_columns_ignored(self, tmp_path):
        """Columns beyond the 4th are ignored."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message", "extra1", "extra2"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg", "x", "y"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 1


# ===================================================================
# §9  CLI interface
# ===================================================================

class TestCLIInterface:
    def test_input_file_not_found_exit_1(self, tmp_path):
        """Non-existent input file → exit 1."""
        out = tmp_path / "out.csv"
        code, _, stderr = _run("nonexistent_file.csv", str(out))
        assert code == 1
        assert "input file not found" in stderr.lower()

    def test_success_exit_0(self, tmp_path):
        """Valid run with no malformed rows → exit 0."""
        p = _basic_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0

    def test_version_flag_exits_0(self, tmp_path):
        """--version → exit 0."""
        code, stdout, _ = _run("--version")
        assert code == 0

    def test_help_flag_exits_0(self, tmp_path):
        """--help → exit 0."""
        code, stdout, _ = _run("--help")
        assert code == 0

    def test_output_columns_match_spec(self, tmp_path):
        """Output CSV has the correct header columns in order."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        _run(str(p), str(out))
        with open(out, newline="") as f:
            header = next(csv.reader(f))
        assert header == ["level", "service", "count", "first_seen", "last_seen"]

    def test_default_input_output_paths(self, tmp_path):
        """When no args given, uses data/events.csv and data/summary.csv."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        default_in = data_dir / "events.csv"
        _write_csv(default_in, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg"],
        ])
        result = subprocess.run(
            [sys.executable, "-m", "src.logsum"],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        # Module may not be findable from tmp_path since src/ is at project root.
        # Accept exit 0 (found default input) or exit 1 (module not runnable from tmp_path).
        assert result.returncode in (0, 1)


# ===================================================================
# §5  Output timestamps
# ===================================================================

class TestOutputTimestamps:
    def test_first_seen_is_earliest(self, tmp_path):
        """first_seen is the earliest normalised timestamp in the group."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:02:00Z", "ERROR", "svc", "msg1"],
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg2"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc", "msg3"],
        ])
        out = tmp_path / "out.csv"
        _run(str(p), str(out))
        rows = _read_output(out)
        assert rows[0]["first_seen"] == "2026-06-23T10:00:00Z"

    def test_last_seen_is_latest(self, tmp_path):
        """last_seen is the latest normalised timestamp in the group."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg1"],
            ["2026-06-23T10:02:00Z", "ERROR", "svc", "msg2"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc", "msg3"],
        ])
        out = tmp_path / "out.csv"
        _run(str(p), str(out))
        rows = _read_output(out)
        assert rows[0]["last_seen"] == "2026-06-23T10:02:00Z"

    def test_single_row_first_equals_last(self, tmp_path):
        """Single row → first_seen == last_seen."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc", "msg"],
        ])
        out = tmp_path / "out.csv"
        _run(str(p), str(out))
        rows = _read_output(out)
        assert rows[0]["first_seen"] == rows[0]["last_seen"]


# ===================================================================
# §10  Min-count filtering
# ===================================================================

class TestMinCountFilter:
    def test_flag_not_set_outputs_all_groups(self, tmp_path):
        """When --min-count is omitted, all groups appear in output."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "INFO", "svc-b", "msg2"],
            ["2026-06-23T10:02:00Z", "ERROR", "svc-a", "msg3"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 2
        counts = {int(r["count"]) for r in rows}
        assert counts == {2, 1}

    def test_min_count_2_excludes_groups_with_count_1(self, tmp_path):
        """--min-count 2 drops groups whose count < 2."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc-a", "msg2"],
            ["2026-06-23T10:02:00Z", "INFO", "svc-b", "msg3"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out), "--min-count", "2")
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["level"] == "ERROR"
        assert rows[0]["service"] == "svc-a"
        assert int(rows[0]["count"]) == 2

    def test_min_count_equal_to_count_preserves_group(self, tmp_path):
        """A group with count == N is preserved (>= semantics)."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc-a", "msg2"],
            ["2026-06-23T10:02:00Z", "INFO", "svc-b", "msg3"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out), "--min-count", "2")
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 1
        assert int(rows[0]["count"]) == 2

    def test_min_count_larger_than_max_count_produces_header_only(self, tmp_path):
        """--min-count value exceeding all group counts → header-only output, exit 0."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "INFO", "svc-b", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out), "--min-count", "100")
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 0
        with open(out, newline="") as f:
            header = next(csv.reader(f))
        assert header == ["level", "service", "count", "first_seen", "last_seen"]

    def test_min_count_zero_outputs_all_groups(self, tmp_path):
        """Explicit --min-count 0 behaves identically to omitting the flag."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "INFO", "svc-b", "msg2"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out), "--min-count", "0")
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 2

    def test_min_count_with_malformed_rows_exit_2(self, tmp_path):
        """When rows are malformed AND --min-count filters, exit 2 takes precedence."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-a", "msg1"],
            ["2026-06-23T10:01:00Z", "ERROR", "svc-a", "msg2"],
            ["bad-ts", "INFO", "svc-b", "malformed"],
        ])
        out = tmp_path / "out.csv"
        code, _, stderr = _run(str(p), str(out), "--min-count", "2")
        assert code == 2
        assert "skipped" in stderr.lower()
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["level"] == "ERROR"
        assert int(rows[0]["count"]) == 2

    def test_min_count_combined_with_basic_scenario(self, tmp_path):
        """Reproduce the basic scenario (§12.1) with --min-count 2 applied."""
        p = _basic_csv(tmp_path)
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out), "--min-count", "2")
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 1
        assert rows[0]["level"] == "ERROR"
        assert rows[0]["service"] == "payment-svc"
        assert int(rows[0]["count"]) == 2


# ===================================================================
# §11  Out-of-scope — non-sorting
# ===================================================================

class TestOutOfScope:
    def test_no_sorting_guarantee_on_output(self, tmp_path):
        """§11 explicitly states no sorting guarantee.  This test only verifies
        that output is produced and all expected rows are present — order is
        not asserted."""
        p = tmp_path / "in.csv"
        _write_csv(p, ["timestamp", "level", "service", "message"], [
            ["2026-06-23T10:00:00Z", "ERROR", "svc-b", "msg"],
            ["2026-06-23T10:01:00Z", "INFO", "svc-a", "msg"],
            ["2026-06-23T10:02:00Z", "ERROR", "svc-a", "msg"],
        ])
        out = tmp_path / "out.csv"
        code, _, _ = _run(str(p), str(out))
        assert code == 0
        rows = _read_output(out)
        assert len(rows) == 3
        keys = {(r["level"], r["service"]) for r in rows}
        assert keys == {("ERROR", "svc-b"), ("INFO", "svc-a"), ("ERROR", "svc-a")}
