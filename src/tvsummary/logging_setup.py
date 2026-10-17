"""Set up logging for the program, called once from main()."""

import logging


def setup_logging(level: str) -> None:
    """Configure the root logger with a plain, readable format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        force=True,
    )
