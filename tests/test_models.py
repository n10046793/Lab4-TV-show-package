"""Tests for the ShowRecord class. No network: the records are hand-made."""

from tvsummary.models import ShowRecord


def test_show_record_keeps_good_values() -> None:
    record = ShowRecord(
        {
            "name": "Dark",
            "genres": ["Drama"],
            "language": "German",
            "rating": {"average": 8.1},
            "premiered": "2017-12-01",
        }
    )
    assert record.name == "Dark"
    assert record.genres == ["Drama"]
    assert record.language == "German"
    assert record.rating == 8.1
    assert record.premiered == "2017-12-01"


def test_show_record_missing_genre_list_becomes_empty() -> None:
    record = ShowRecord({"name": "Mystery Show", "language": "English"})
    assert record.genres == []


def test_show_record_missing_rating_becomes_none() -> None:
    record = ShowRecord({"name": "Unrated Show", "genres": ["Drama"]})
    assert record.rating is None


def test_show_record_missing_name_becomes_unknown() -> None:
    record = ShowRecord({"genres": ["Drama"]})
    assert record.name == "Unknown"
