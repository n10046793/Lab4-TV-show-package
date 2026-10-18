"""Tests for downloading, without touching the network."""

import pytest
import requests

from tvsummary.errors import BadResponseError, DownloadError
from tvsummary.models import ShowRecord
from tvsummary.settings import Settings
from tvsummary.sources import TVMazeSource


def make_settings() -> Settings:
    return Settings(
        source_url="https://example.com/shows",
        timeout=10,
        output_folder="data/processed",
        seed=7,
        sample_size=5,
        log_level="INFO",
    )


class FakeResponse:
    """Pretends to be the answer from requests.get."""

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        pass

    def json(self) -> object:
        return self.payload


def test_fetch_returns_show_records(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse([{"name": "Dark", "genres": ["Drama"]}])

    monkeypatch.setattr(requests, "get", fake_get)
    records = TVMazeSource(make_settings()).fetch()
    assert len(records) == 1
    assert isinstance(records[0], ShowRecord)
    assert records[0].name == "Dark"


def test_fetch_raises_download_error_when_the_network_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        raise requests.ConnectionError("no internet")

    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(DownloadError, match="Could not download"):
        TVMazeSource(make_settings()).fetch()


def test_fetch_raises_bad_response_error_for_wrong_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse({"not": "a list"})

    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(BadResponseError, match="not a list"):
        TVMazeSource(make_settings()).fetch()


def test_fetch_raises_bad_response_error_for_non_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class BadJsonResponse(FakeResponse):
        def json(self) -> object:
            raise ValueError("not JSON")

    def fake_get(url: str, timeout: int) -> FakeResponse:
        return BadJsonResponse([])

    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(BadResponseError, match="JSON"):
        TVMazeSource(make_settings()).fetch()
