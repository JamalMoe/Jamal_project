
"""Logging configuration for Jamal Project."""

import logging
from pathlib import Path


def setup_logger(
    name: str = "JamalProject",
    level: str = "INFO",
    log_file: str = "JamalProject.log",
) -> logging.Logger:
    """Configure and return the application logger."""

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers.
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    # Create log directory if necessary.
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Save logs to a file.
    file_handler = logging.FileHandler(
        log_path, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Also display logs in the terminal.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
if __name__ == "__main__":
    logger = setup_logger()

    logger.debug("Debug message")
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("An error occurred")
    logger.critical("Critical failure")