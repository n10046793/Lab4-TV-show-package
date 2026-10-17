"""Thin entry point: wire the package pieces together."""

import logging
import sys

from tvsummary import OUTPUT_PATH, TVMazeSource, build_summary, write_summary
from tvsummary.errors import TvSummaryError
from tvsummary.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main() -> int:
    """Download the records, summarize them and write the summary file."""
    setup_logging("INFO")
    try:
        records = TVMazeSource().fetch()
    except TvSummaryError as exc:
        logger.error("The run failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if not records:
        logger.warning("No show records were downloaded; the summary will be empty.")
    summary = build_summary(records)
    write_summary(summary, OUTPUT_PATH)
    print(f"Processed {summary['records_processed']} TV show records.")
    print(f"Most common genre: {summary['most_common_genre']}.")
    print(f"Summary written to {OUTPUT_PATH}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
