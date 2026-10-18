"""Tests for main(): exit codes and the Error: line. No network."""

from pathlib import Path

import pytest

from tvsummary.main import main
from tvsummary.models import ShowRecord
from tvsummary.sources import TVMazeSource


def test_main_returns_1_and_prints_error_for_missing_config(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = main(["--config", str(tmp_path / "missing.toml")])
    assert code == 1
    err = capsys.readouterr().err
    assert any(line.startswith("Error:") for line in err.splitlines())


def test_main_returns_0_and_writes_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config = tmp_path / "tvsummary.toml"
    out = tmp_path / "out"
    config.write_text(
        'source_url = "https://example.com"\n'
        "timeout = 10\n"
        f'output_folder = "{out.as_posix()}"\n'
        "seed = 7\n"
        "sample_size = 2\n"
        'log_level = "INFO"\n',
        encoding="utf-8",
    )
    records = [
        ShowRecord({"name": "Show A", "genres": ["Drama"]}),
        ShowRecord({"name": "Show B", "genres": ["Comedy"]}),
    ]
    monkeypatch.setattr(TVMazeSource, "fetch", lambda self: records)
    code = main(["--config", str(config)])
    assert code == 0
    assert (out / "summary.json").exists()
    assert (out / "run_info.json").exists()
    printed = capsys.readouterr().out
    assert "Processed 2 TV show records." in printed
