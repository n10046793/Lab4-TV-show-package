"""Shared fixtures for the test suite."""

import pytest

from tvsummary.models import ShowRecord


@pytest.fixture
def sample_records() -> list[ShowRecord]:
    """A small hand-made list of show records for the tests."""
    return [
        ShowRecord(
            {
                "name": "Show A",
                "genres": ["Drama", "Comedy"],
                "language": "English",
                "rating": {"average": 8.5},
                "premiered": "2001-05-01",
            }
        ),
        ShowRecord(
            {
                "name": "Show B",
                "genres": ["Drama"],
                "language": "English",
                "rating": {"average": 7.5},
                "premiered": "1995-03-10",
            }
        ),
        ShowRecord(
            {
                "name": "Show C",
                "genres": ["Comedy"],
                "language": "French",
                "rating": {"average": 9.0},
                "premiered": "2010-11-20",
            }
        ),
        ShowRecord(
            {
                "name": "Show D",
                "genres": [],
                "language": "English",
                "rating": {"average": None},
                "premiered": None,
            }
        ),
    ]
