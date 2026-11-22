
import pytest

from Jamal_project.exceptions import (
    JamalProjectError,
    ScanTargetError,
    InvalidPortError,
    APIKeyMissingError,
    APIRequestError,
    APIResponseError,
    NetworkDiscoveryError,
    PacketCaptureError,
    ConfigurationError,
)


def test_all_custom_exceptions_inherit_from_base():
    exceptions = [
        ScanTargetError,
        InvalidPortError,
        APIKeyMissingError,
        APIRequestError,
        APIResponseError,
        NetworkDiscoveryError,
        PacketCaptureError,
        ConfigurationError,
    ]

    for exception in exceptions:
        assert issubclass(exception, JamalProjectError)


def test_base_exception_inherits_from_exception():
    assert issubclass(JamalProjectError, Exception)


def test_custom_exception_can_be_raised():
    with pytest.raises(ScanTargetError, match="Invalid target"):
        raise ScanTargetError("Invalid target")


def test_custom_exception_message():
    error = ConfigurationError("Configuration file missing")

    assert str(error) == "Configuration file missing"
