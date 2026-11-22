
import json
import pytest
import socket

from Jamal_project.scanner_cli import (
    ThreadedScanner,
    parse_ports,
    build_parser,
)


# =====================================
# TEST parse_ports()
# =====================================

def test_parse_ports_range():
    assert parse_ports("1-5") == [1, 2, 3, 4, 5]


def test_parse_ports_list():
    assert parse_ports("22,80,443") == [22, 80, 443]


def test_parse_ports_single():
    assert parse_ports("80") == [80]


# =====================================
# TEST build_parser()
# =====================================

def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["127.0.0.1"])

    assert args.target == "127.0.0.1"
    assert args.ports == "1-1024"
    assert args.threads == 100
    assert args.output is None


def test_build_parser_custom_arguments():
    parser = build_parser()

    args = parser.parse_args([
        "127.0.0.1",
        "-p", "80,443",
        "-t", "20",
        "-o", "results.json"
    ])

    assert args.ports == "80,443"
    assert args.threads == 20
    assert args.output == "results.json"


# =====================================
# TEST scan_port()
# =====================================

def test_scan_port_open(mocker):
    mocker.patch(
        "Jamal_project.scanner_cli.socket.create_connection"
    )

    assert ThreadedScanner.scan_port("127.0.0.1", 80) is True


def test_scan_port_closed(mocker):
    mocker.patch(
        "Jamal_project.scanner_cli.socket.create_connection",
        side_effect=ConnectionRefusedError
    )

    assert ThreadedScanner.scan_port("127.0.0.1", 80) is False


def test_scan_port_timeout(mocker):
    mocker.patch(
        "Jamal_project.scanner_cli.socket.create_connection",
        side_effect=socket.timeout
    )

    assert ThreadedScanner.scan_port("127.0.0.1", 80) is False


# =====================================
# TEST threaded_scan()
# =====================================

def test_threaded_scan(mocker):
    mocker.patch.object(
        ThreadedScanner,
        "scan_port",
        side_effect=lambda target, port, timeout: port in [80, 443]
    )

    result = ThreadedScanner.threaded_scan(
        "127.0.0.1",
        [443, 22, 80],
        max_threads=2
    )

    assert result == [80, 443]


def test_threaded_scan_invalid_target():
    with pytest.raises(ValueError, match="target hostname or IP"):
        ThreadedScanner.threaded_scan("", [80])


def test_threaded_scan_invalid_threads():
    with pytest.raises(ValueError, match="Thread count"):
        ThreadedScanner.threaded_scan(
            "127.0.0.1",
            [80],
            max_threads=0
        )


def test_threaded_scan_invalid_ports(mocker):
    mocker.patch.object(
        ThreadedScanner,
        "scan_port",
        return_value=True
    )

    result = ThreadedScanner.threaded_scan(
        "127.0.0.1",
        [0, 80, 65536],
        max_threads=2
    )

    assert result == [80]


# =====================================
# TEST main()
# =====================================

def test_main_json_output(mocker, tmp_path, capsys):
    output_file = tmp_path / "results.json"

    mocker.patch(
        "sys.argv",
        [
            "scanner_cli",
            "127.0.0.1",
            "-p", "80,443",
            "-o", str(output_file)
        ]
    )

    mocker.patch.object(
        ThreadedScanner,
        "threaded_scan",
        return_value=[80]
    )

    ThreadedScanner.main()

    captured = capsys.readouterr()

    assert "Scanning 127.0.0.1" in captured.out
    assert "Open ports: [80]" in captured.out

    with open(output_file, encoding="utf-8") as file:
        results = json.load(file)

    assert results == {
        "target": "127.0.0.1",
        "open_ports": [80]
    }
