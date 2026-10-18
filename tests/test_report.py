"""Tests for building the summary and writing the files. No network."""

import json
from pathlib import Path

from tvsummary.models import ShowRecord
from tvsummary.report import (
    build_summary,
    featured_shows,
    write_run_info,
    write_summary,
)
from tvsummary.settings import Settings


def make_settings(seed: int = 7, sample_size: int = 2) -> Settings:
    return Settings(
        source_url="https://example.com",
        timeout=10,
        output_folder="data/processed",
        seed=seed,
        sample_size=sample_size,
        log_level="INFO",
    )


def test_build_summary_has_all_expected_keys(
    sample_records: list[ShowRecord],
) -> None:
    summary = build_summary(sample_records, make_settings())
    assert summary["records_processed"] == 4
    assert summary["source_url"] == "https://example.com"
    assert summary["most_common_genre"] == "Drama"
    assert summary["distinct_genres"] == ["Comedy", "Drama"]
    assert "featured_shows" in summary


def test_featured_shows_same_seed_gives_same_list(
    sample_records: list[ShowRecord],
) -> None:
    settings = make_settings()
    first = featured_shows(sample_records, settings)
    second = featured_shows(sample_records, settings)
    assert first == second
    assert len(first) == 2
    assert set(first) <= {"Show A", "Show B", "Show C", "Show D"}


def test_write_summary_writes_json(
    tmp_path: Path, sample_records: list[ShowRecord]
) -> None:
    summary = build_summary(sample_records, make_settings())
    target = tmp_path / "out" / "summary.json"
    write_summary(summary, target)
    loaded = json.loads(target.read_text(encoding="utf-8"))
    assert loaded["records_processed"] == 4


def test_write_run_info_writes_json_next_to_summary(
    tmp_path: Path, sample_records: list[ShowRecord]
) -> None:
    settings = make_settings()
    summary_path = tmp_path / "out" / "summary.json"
    write_summary(build_summary(sample_records, settings), summary_path)
    write_run_info(summary_path, settings)
    info_path = tmp_path / "out" / "run_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8"))
    assert info["settings"]["seed"] == 7
    assert "python_version" in info
    assert "pytest_version" in info
    assert "mypy_version" in info
    assert "ruff_version" in info
