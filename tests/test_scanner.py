
import pytest
import socket

from Jamal_project.scanner import PortScanner


def test_scanner_initialization():
    scanner = PortScanner(
        target="127.0.0.1",
        ports=[80, 443]
    )

    assert scanner.target == "127.0.0.1"
    assert scanner.ports == [80, 443]
    assert scanner.timeout == 0.5
    assert scanner.open_ports == []


def test_scanner_finds_open_ports(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.__enter__.return_value = fake_socket
    fake_socket.connect_ex.side_effect = [0, 1]

    mocker.patch(
        "Jamal_project.scanner.socket.socket",
        return_value=fake_socket
    )

    scanner = PortScanner(
        target="127.0.0.1",
        ports=[80, 443]
    )

    result = scanner.scan()

    assert result == [80]
    assert scanner.open_ports == [80]


def test_scanner_no_open_ports(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.__enter__.return_value = fake_socket
    fake_socket.connect_ex.return_value = 1

    mocker.patch(
        "Jamal_project.scanner.socket.socket",
        return_value=fake_socket
    )

    scanner = PortScanner(
        target="127.0.0.1",
        ports=[80, 443]
    )

    result = scanner.scan()

    assert result == []


def test_scanner_invalid_hostname(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.__enter__.return_value = fake_socket
    fake_socket.connect_ex.side_effect = socket.gaierror

    mocker.patch(
        "Jamal_project.scanner.socket.socket",
        return_value=fake_socket
    )

    scanner = PortScanner(
        target="invalid-host",
        ports=[80]
    )

    with pytest.raises(ValueError, match="Could not resolve host"):
        scanner.scan()


def test_scanner_report(capsys):
    scanner = PortScanner(
        target="127.0.0.1",
        ports=[80, 443]
    )

    scanner.open_ports = [80, 443]

    scanner.report()

    captured = capsys.readouterr()

    assert "Scan of 127.0.0.1 completed at" in captured.out
    assert "Open ports: [80, 443]" in captured.out
    assert "80/tcp open" in captured.out
    assert "443/tcp open" in captured.out


def test_scanner_report_no_open_ports(capsys):
    scanner = PortScanner(
        target="127.0.0.1",
        ports=[80, 443]
    )

    scanner.report()

    captured = capsys.readouterr()

    assert "No open ports found." in captured.out
