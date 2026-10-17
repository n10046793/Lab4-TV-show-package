"""Load the program's settings from a TOML file."""

import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tvsummary.errors import SettingsError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    """Everything the program needs to know to do one run."""

    source_url: str
    timeout: int
    output_folder: str
    seed: int
    sample_size: int
    log_level: str


_REQUIRED_KEYS = (
    "source_url",
    "timeout",
    "output_folder",
    "seed",
    "sample_size",
    "log_level",
)


def load_settings(path: str | Path) -> Settings:
    """Read the TOML file at path and return the settings.

    Raises SettingsError if the file is missing, unreadable,
    or does not contain every required key.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise SettingsError(f"Could not read the settings file: {path}.") from exc
    try:
        data: dict[str, Any] = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise SettingsError(f"The settings file is not valid TOML: {path}.") from exc
    missing = [key for key in _REQUIRED_KEYS if key not in data]
    if missing:
        raise SettingsError(f"The settings file is missing: {', '.join(missing)}.")
    settings = Settings(
        source_url=data["source_url"],
        timeout=data["timeout"],
        output_folder=data["output_folder"],
        seed=data["seed"],
        sample_size=data["sample_size"],
        log_level=data["log_level"],
    )
    logger.info("Loaded the settings from %s", path)
    return settings
