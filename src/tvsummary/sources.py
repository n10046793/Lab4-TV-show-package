"""Fetching records. This is the only module that uses requests."""

import logging

import requests

from tvsummary.errors import BadResponseError, DownloadError
from tvsummary.models import ShowRecord
from tvsummary.settings import Settings

logger = logging.getLogger(__name__)


class TVMazeSource:
    """Downloads TV show records from the TVMaze API.

    Returns ShowRecord objects, not raw dictionaries.
    """

    def __init__(self, settings: Settings) -> None:
        """Save the settings this source should download with."""
        self.settings = settings

    def fetch(self) -> list[ShowRecord]:
        """Download the records and return them as ShowRecord objects.

        Raises DownloadError if the download fails, and BadResponseError
        if the answer does not look like a list of show dictionaries.
        """
        logger.debug("Downloading show records from %s", self.settings.source_url)
        try:
            response = requests.get(
                self.settings.source_url, timeout=self.settings.timeout
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise DownloadError(
                f"Could not download the show records from {self.settings.source_url}."
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
        logger.info("Downloaded %d show records.", len(records))
        return records
