import pytest
import socket

import pytest

from Jamal_project.multithreading import check_port, threaded_scan



def test_check_port_open(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.connect_ex.return_value = 0

    mock_socket = mocker.patch(
        "Jamal_project.multithreading.socket.socket"
    )

    mock_socket.return_value.__enter__.return_value = fake_socket

    result = check_port("127.0.0.1", 80)

    assert result == 80


def test_check_port_closed(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.connect_ex.return_value = 1

    mock_socket = mocker.patch(
        "Jamal_project.multithreading.socket.socket"
    )

    mock_socket.return_value.__enter__.return_value = fake_socket

    result = check_port("127.0.0.1", 80)

    assert result is None


def test_check_port_timeout(mocker):
    fake_socket = mocker.MagicMock()
    fake_socket.connect_ex.side_effect = socket.timeout

    mock_socket = mocker.patch(
        "Jamal_project.multithreading.socket.socket"
    )

    mock_socket.return_value.__enter__.return_value = fake_socket

    with pytest.raises(socket.timeout):
        check_port("127.0.0.1", 80)



def test_threaded_scan(mocker):
    mocker.patch(
        "Jamal_project.multithreading.check_port",
        side_effect=lambda target, port: port if port in [80, 443] else None
    )

    result = threaded_scan(
        target="127.0.0.1",
        ports=[443, 22, 80],
        max_threads=2
    )

    assert result == [80, 443]


def test_threaded_scan_no_open_ports(mocker):
    mocker.patch(
        "Jamal_project.multithreading.check_port",
        return_value=None
    )

    result = threaded_scan(
        target="127.0.0.1",
        ports=[22, 80, 443],
        max_threads=2
    )

    assert result == []
