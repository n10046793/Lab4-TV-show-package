"""Run the program from the command line: python -m tvsummary.main."""

import argparse
import logging
import sys
from pathlib import Path

from tvsummary.errors import SettingsError, TvSummaryError
from tvsummary.logging_setup import setup_logging
from tvsummary.report import build_summary, write_run_info, write_summary
from tvsummary.settings import load_settings
from tvsummary.sources import TVMazeSource

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Summarize TV show records from the TVMaze API."
    )
    parser.add_argument(
        "--config",
        default="config/tvsummary.toml",
        help="Path to the TOML settings file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the whole pipeline. Returns 0 on success, 1 on expected failure."""
    args = parse_args(argv)
    try:
        settings = load_settings(args.config)
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
