
"""Input validation utilities for Jamal Project."""

import ipaddress


def is_valid_ip(value: str) -> bool:
    """Return True if value is a valid IPv4 or IPv6 address."""

    try:
        ipaddress.ip_address(value)
        return True

    except ValueError:
        return False
