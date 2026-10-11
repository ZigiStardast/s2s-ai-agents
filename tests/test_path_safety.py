import pytest

from src.tools import read_file, set_scenario


def setup_function():
    set_scenario("booking_bug")


def test_rejects_parent_traversal():
    with pytest.raises(ValueError):
        read_file("../README.md")


def test_rejects_absolute_path():
    with pytest.raises(ValueError):
        read_file("C:/Windows/win.ini")


def test_cannot_read_env():
    with pytest.raises(ValueError):
        read_file(".env")
