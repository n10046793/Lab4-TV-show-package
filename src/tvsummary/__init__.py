"""tvsummary: summarize TV show records from the TVMaze API."""

from tvsummary.aggregations import (
    Aggregation,
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.errors import (
    BadResponseError,
    DownloadError,
    SettingsError,
    TvSummaryError,
)
from tvsummary.models import ShowRecord
from tvsummary.report import build_summary, write_run_info, write_summary
from tvsummary.settings import Settings, load_settings
from tvsummary.sources import TVMazeSource

__all__ = [
    "ShowRecord",
    "TVMazeSource",
    "Aggregation",
    "AvgRatingByLanguage",
    "ShowsPerDecade",
    "ShowsPerGenre",
    "build_summary",
    "write_summary",
    "write_run_info",
    "TvSummaryError",
    "DownloadError",
    "BadResponseError",
    "SettingsError",
    "Settings",
    "load_settings",
]
