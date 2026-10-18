"""Tests for loading settings from a TOML file."""

from pathlib import Path

import pytest

from tvsummary.errors import SettingsError
from tvsummary.settings import load_settings


def write_toml(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_load_settings_reads_every_key(tmp_path: Path) -> None:
    config = write_toml(
        tmp_path / "tvsummary.toml",
        'source_url = "https://example.com"\n'
        "timeout = 10\n"
        'output_folder = "data/processed"\n'
        "seed = 7\n"
        "sample_size = 5\n"
        'log_level = "INFO"\n',
    )
    settings = load_settings(config)
    assert settings.source_url == "https://example.com"
    assert settings.timeout == 10
    assert settings.output_folder == "data/processed"
    assert settings.seed == 7
    assert settings.sample_size == 5
    assert settings.log_level == "INFO"


def test_load_settings_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(SettingsError, match="Could not read"):
        load_settings(tmp_path / "missing.toml")


def test_load_settings_incomplete_file_raises(tmp_path: Path) -> None:
    config = write_toml(
        tmp_path / "tvsummary.toml", 'source_url = "https://example.com"\n'
    )
    with pytest.raises(SettingsError, match="missing"):
        load_settings(config)


def test_load_settings_invalid_toml_raises(tmp_path: Path) -> None:
    config = write_toml(tmp_path / "tvsummary.toml", "not = [valid toml\n")
    with pytest.raises(SettingsError, match="not valid TOML"):
        load_settings(config)
