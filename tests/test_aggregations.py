"""Tests for the three aggregation classes. No network."""

import pytest

from tvsummary.aggregations import (
    AvgRatingByLanguage,
    ShowsPerDecade,
    ShowsPerGenre,
)
from tvsummary.models import ShowRecord
from tvsummary.report import most_common_genre


def test_shows_per_genre_counts_each_genre(
    sample_records: list[ShowRecord],
) -> None:
    assert ShowsPerGenre().compute(sample_records) == {"Drama": 2, "Comedy": 2}


def test_avg_rating_by_language_skips_missing_ratings(
    sample_records: list[ShowRecord],
) -> None:
    assert AvgRatingByLanguage().compute(sample_records) == {
        "English": 8.0,
        "French": 9.0,
    }


def test_shows_per_decade_groups_by_decade(
    sample_records: list[ShowRecord],
) -> None:
    assert ShowsPerDecade().compute(sample_records) == {
        "2000s": 1,
        "1990s": 1,
        "2010s": 1,
    }


@pytest.mark.parametrize(
    "counts, expected",
    [
        ({"Drama": 3, "Comedy": 1}, "Drama"),
        ({"Comedy": 5}, "Comedy"),
        ({}, None),
    ],
)
def test_most_common_genre(counts: dict[str, int], expected: str | None) -> None:
    assert most_common_genre(counts) == expected
