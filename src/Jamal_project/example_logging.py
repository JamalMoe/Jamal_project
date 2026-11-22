
"""Example demonstrating logging and custom exception handling."""

import logging
import ipaddress

from Jamal_project.config import load_config
from Jamal_project.logger import setup_logger
from Jamal_project.exceptions import ScanTargetError


# Load application configuration.
config = load_config()

# Configure application logging.
logging_config = config.get("logging", {})

logger = setup_logger(
    name="JamalProject.scan",
    level=logging_config.get("level", "INFO"),
    log_file=logging_config.get("file", "JamalProject.log"),
)


def scan_target(ip: str) -> None:
    """Validate a target and demonstrate logging."""

    logger.info("Starting scan of %s", ip)

    try:
        # Validate the supplied IP address.
        ipaddress.ip_address(ip)

        # Scanning logic would go here.
        logger.info("Scan of %s completed successfully", ip)

    except ValueError as exc:
        error = ScanTargetError(
            f"{ip} is not a valid IP address"
        )

        logger.error("Scan aborted: %s", error)
        raise error from exc


if __name__ == "__main__":
    scan_target("192.168.1.10")
