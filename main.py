"""Thin entry point: wire the package pieces together."""

import logging
import sys
from pathlib import Path

from tvsummary import TVMazeSource, build_summary, write_run_info, write_summary
from tvsummary.errors import SettingsError, TvSummaryError
from tvsummary.logging_setup import setup_logging
from tvsummary.settings import load_settings

logger = logging.getLogger(__name__)


def main() -> int:
    """Download the records, summarize them and write the summary file."""
    try:
        settings = load_settings("config/tvsummary.toml")
    except SettingsError as exc:
        setup_logging("INFO")
        logger.error("Could not load the settings: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    setup_logging(settings.log_level)
    try:
        records = TVMazeSource(settings).fetch()
    except TvSummaryError as exc:
        logger.error("The run failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if not records:
        logger.warning("No show records were downloaded; the summary will be empty.")
    summary = build_summary(records, settings)
    output_path = Path(settings.output_folder) / "summary.json"
    write_summary(summary, output_path)
    write_run_info(output_path, settings)
    print(f"Processed {summary['records_processed']} TV show records.")
    print(f"Most common genre: {summary['most_common_genre']}.")
    print(f"Summary written to {output_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
