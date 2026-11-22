
"""Tests for Jamal Project validation utilities."""

from Jamal_project.validators import is_valid_ip


def test_valid_ipv4():
    assert is_valid_ip("192.168.1.10") is True


def test_valid_ipv6():
    assert is_valid_ip("2001:db8::1") is True


def test_invalid_ip():
    assert is_valid_ip("999.999.999.999") is False


def test_invalid_string():
    assert is_valid_ip("hello") is False


def test_empty_string():
    assert is_valid_ip("") is False
