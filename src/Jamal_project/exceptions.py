
"""Custom exceptions used across Jamal Project."""


class JamalProjectError(Exception):
    """Base exception for Jamal Project."""


class ScanTargetError(JamalProjectError):
    """Raised when a scan target is invalid or cannot be resolved."""


class InvalidPortError(JamalProjectError):
    """Raised when an invalid TCP port is supplied."""


class APIKeyMissingError(JamalProjectError):
    """Raised when a required API key is missing."""


class APIRequestError(JamalProjectError):
    """Raised when an external API request fails."""


class APIResponseError(JamalProjectError):
    """Raised when an API returns an unexpected response."""


class NetworkDiscoveryError(JamalProjectError):
    """Raised when network discovery fails."""


class PacketCaptureError(JamalProjectError):
    """Raised when packet capture or transmission fails."""


class ConfigurationError(JamalProjectError):
    """Raised when application configuration fails."""
