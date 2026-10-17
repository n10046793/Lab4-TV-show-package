"""Build the summary dictionary and write it to a JSON file."""

import importlib.metadata
import json
import logging
import platform
import random
from dataclasses import asdict
from pathlib import Path

from tvsummary.aggregations import (
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)

logger = logging.getLogger(__name__)


def most_common_genre(genre_counts):
    """Return the genre with the highest count."""
    top_genre = None
    top_count = 0
    for genre, count in genre_counts.items():
        if count > top_count:
            top_genre = genre
            top_count = count
    return top_genre


def featured_shows(records, settings):
    """Pick sample_size show names using the seeded random generator.

    The same seed always gives the same list.
    """
    names = [record.name for record in records]
    count = min(settings.sample_size, len(names))
    return random.Random(settings.seed).sample(names, count)


def build_summary(records, settings):
    """Combine the aggregations into one dictionary ready to write.

    Each aggregation is asked for its answer through the same
    compute() method; the loop never checks which subclass it holds.
    """
    logger.info("Building the summary from %d records.", len(records))
    aggregations = [ShowsPerGenre(), AvgRatingByLanguage(), ShowsPerDecade()]

    results = {}
    for aggregation in aggregations:
        results[aggregation.name] = aggregation.compute(records)

    genre_counts = results["shows_per_genre"]

    return {
        "source_url": settings.source_url,
        "records_processed": len(records),
        "shows_per_genre": genre_counts,
        "distinct_genres": sorted(genre_counts),
        "most_common_genre": most_common_genre(genre_counts),
        "average_rating_by_language": results["average_rating_by_language"],
        "shows_per_decade": results["shows_per_decade"],
        "featured_shows": featured_shows(records, settings),
    }


def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logger.info("Wrote the summary to %s", path)


def write_run_info(summary_path, settings):
    """Write run_info.json next to the summary file.

    It records the settings used, the Python version, and the
    versions of pytest, mypy and ruff.
    """
    info = {
        "settings": asdict(settings),
        "python_version": platform.python_version(),
        "pytest_version": _tool_version("pytest"),
        "mypy_version": _tool_version("mypy"),
        "ruff_version": _tool_version("ruff"),
    }
    target = Path(summary_path).parent / "run_info.json"
    target.write_text(json.dumps(info, indent=2), encoding="utf-8")
    logger.info("Wrote the run info to %s", target)


def _tool_version(name):
    """Return the installed version of a tool, or 'unknown'."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"
