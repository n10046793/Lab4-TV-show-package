"""The package's own exceptions.

Every error the program expects is one of these, so main() can
catch the base class and report any of them the same way.
"""


class TvSummaryError(Exception):
    """Base class for every error this package raises on purpose."""


class DownloadError(TvSummaryError):
    """The show records could not be downloaded."""


class BadResponseError(TvSummaryError):
    """The API answered, but its data had the wrong shape."""


class SettingsError(TvSummaryError):
    """The settings file is missing or cannot be used."""
