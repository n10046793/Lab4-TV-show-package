"""Thin entry point: wire the package pieces together."""

import sys

from tvsummary import OUTPUT_PATH, TVMazeSource, build_summary, write_summary
from tvsummary.errors import TvSummaryError


def main() -> int:
    """Download the records, summarize them and write the summary file."""
    try:
        records = TVMazeSource().fetch()
    except TvSummaryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    summary = build_summary(records)
    write_summary(summary, OUTPUT_PATH)
    print(f"Processed {summary['records_processed']} TV show records.")
    print(f"Most common genre: {summary['most_common_genre']}.")
    print(f"Summary written to {OUTPUT_PATH}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
