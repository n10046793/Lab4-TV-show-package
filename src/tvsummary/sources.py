"""Fetching records. This is the only module that uses requests."""

import requests

from tvsummary.config import API_URL, REQUEST_TIMEOUT
from tvsummary.errors import BadResponseError, DownloadError
from tvsummary.models import ShowRecord


class TVMazeSource:
    """Downloads TV show records from the TVMaze API.

    Returns ShowRecord objects, not raw dictionaries.
    """

    def __init__(self) -> None:
        """Save the URL and timeout from the config module."""
        self.url = API_URL
        self.timeout = REQUEST_TIMEOUT

    def fetch(self) -> list[ShowRecord]:
        """Download the records and return them as ShowRecord objects.

        Raises DownloadError if the download fails, and BadResponseError
        if the answer does not look like a list of show dictionaries.
        """
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise DownloadError(
                f"Could not download the show records from {self.url}."
            ) from exc
        try:
            items = response.json()
        except ValueError as exc:
            raise BadResponseError("The API did not answer with JSON.") from exc
        if not isinstance(items, list):
            raise BadResponseError("The API answer was not a list of shows.")
        records = []
        for item in items:
            if not isinstance(item, dict):
                raise BadResponseError("One of the shows was not a dictionary.")
            records.append(ShowRecord(item))
        return records

