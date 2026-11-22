"""Command line interface for the threaded port scanner."""

import argparse
import json
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed




class ThreadedScanner:
    """Threaded TCP port scanner implementation."""

    @staticmethod
    def main():
        """Parse command-line arguments and run the port scan."""
        parser = build_parser()
        args = parser.parse_args()

        try:
            ports = parse_ports(args.ports)
            open_ports = ThreadedScanner.threaded_scan(
                args.target,
                ports,
                max_threads=args.threads,
            )
        except ValueError as exc:
            parser.error(str(exc))

        print(
            f"Scanning {args.target}, {len(ports)} ports, "
            f"{args.threads} threads"
        )
        print(f"Open ports: {open_ports}")

        if args.output:
            results = {"target": args.target, "open_ports": open_ports}
            with open(args.output, "w", encoding="utf-8") as output_file:
                json.dump(results, output_file, indent=2)
            print(f"Results saved to {args.output}")

    @staticmethod
    def scan_port(target: str, port: int, timeout: float = 0.5) -> bool:
        """Return True when a TCP connection can be established on a port."""
        try:
            with socket.create_connection((target, port), timeout=timeout):
                return True
        except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
            return False

    @classmethod
    def threaded_scan(
        cls,
        target: str,
        ports: list[int],
        max_threads: int = 100,
        timeout: float = 0.5,
    ) -> list[int]:
        """Scan ports concurrently and return the sorted open ports."""
        if not target:
            raise ValueError("A target hostname or IP address is required")
        if max_threads < 1:
            raise ValueError("Thread count must be at least 1")

        valid_ports = sorted({p for p in ports if 1 <= p <= 65535})
        open_ports: list[int] = []

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {
                executor.submit(cls.scan_port, target, port, timeout): port
                for port in valid_ports
            }
            for future in as_completed(futures):
                if future.result():
                    open_ports.append(futures[future])

        return sorted(open_ports)


def parse_ports(port_string: str) -> list[int]:
    """Convert a string like '1-100' or '22,80,443' into a list of ints."""
    if "-" in port_string:
        start, end = port_string.split("-")
        return list(range(int(start), int(end) + 1))
    return [int(p) for p in port_string.split(",")]

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scanner_cli",
        description="A threaded TCP port scanner for authorised targets only.",
    )

    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument(
        "-p", "--ports", default="1-1024",
        help="Port range or comma separated list, default 1-1024",
    )

    parser.add_argument(
        "-t", "--threads", type=int, default=100,
        help="Number of worker threads, default 100",
    )

    parser.add_argument("-o", "--output", help="Save results as JSON to this file")
    return parser

if __name__ == "__main__":
    ThreadedScanner.main()