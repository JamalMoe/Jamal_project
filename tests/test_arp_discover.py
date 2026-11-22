
from unittest.mock import MagicMock

from Jamal_project.arp_discover import arp_scan


def test_arp_scan_returns_discovered_devices(mocker):
    fake_response = [
        (
            MagicMock(),
            MagicMock(
                psrc="192.168.1.10",
                hwsrc="AA:BB:CC:DD:EE:FF"
            )
        ),
        (
            MagicMock(),
            MagicMock(
                psrc="192.168.1.20",
                hwsrc="11:22:33:44:55:66"
            )
        )
    ]

    mocker.patch(
        "Jamal_project.arp_discover.srp",
        return_value=(fake_response, [])
    )

    result = arp_scan("192.168.1.0/24")

    assert len(result) == 2
    assert result[0]["ip"] == "192.168.1.10"
    assert result[0]["mac"] == "AA:BB:CC:DD:EE:FF"
    assert result[1]["ip"] == "192.168.1.20"
    assert result[1]["mac"] == "11:22:33:44:55:66"


def test_arp_scan_returns_empty_list_when_no_devices(mocker):
    mocker.patch(
        "Jamal_project.arp_discover.srp",
        return_value=([], [])
    )

    result = arp_scan("192.168.1.0/24")

    assert result == []


def test_arp_scan_calls_srp_with_expected_arguments(mocker):
    fake_srp = mocker.patch(
        "Jamal_project.arp_discover.srp",
        return_value=([], [])
    )

    arp_scan("192.168.1.0/24")

    fake_srp.assert_called_once()

    args, kwargs = fake_srp.call_args

    assert kwargs["timeout"] == 2
    assert kwargs["verbose"] is False
