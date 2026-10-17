"""tvsummary: summarize TV show records from the TVMaze API."""

from tvsummary.aggregations import (
    Aggregation,
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.config import API_URL, OUTPUT_PATH, REQUEST_TIMEOUT
from tvsummary.errors import (
    BadResponseError,
    DownloadError,
    SettingsError,
    TvSummaryError,
)
from tvsummary.models import ShowRecord
from tvsummary.report import build_summary, write_summary
from tvsummary.sources import TVMazeSource

__all__ = [
    "API_URL",
    "OUTPUT_PATH",
    "REQUEST_TIMEOUT",
    "ShowRecord",
    "TVMazeSource",
    "Aggregation",
    "AvgRatingByLanguage",
    "ShowsPerDecade",
    "ShowsPerGenre",
    "build_summary",
    "write_summary",
    "TvSummaryError",
    "DownloadError",
    "BadResponseError",
    "SettingsError",
]
