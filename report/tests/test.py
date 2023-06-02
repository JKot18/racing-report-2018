import unittest
import pytest

from pathlib import Path
from report.src._.main import print_report, print_driver_info, build_report

# from ..src._.main import print_report, print_driver_info, build_report
from typing import NoReturn


def test_print_report(capsys: pytest.CaptureFixture) -> NoReturn:
    """
    Test the print_report function. Capture print output and compare with the expected one.
    """
    test_folder = Path(__file__).resolve().parent.parent / 'tests' / 'test_data'
    print_report(test_folder, 'asc')
    captured = capsys.readouterr()
    expected_output = "1. RGH | Romain Grosjean      | HAAS FERRARI                   | 0:01:12.930000\n2. MES | Marcus Ericsson      | SAUBER FERRARI                 | 0:01:13.265000\n"
    assert captured.out == expected_output


def test_print_driver_info(capsys: pytest.CaptureFixture) -> NoReturn:
    """
    Test the print_driver_info function. Capture print output and compare with the expected one.
    """
    test_folder = Path(__file__).resolve().parent.parent / 'tests' / 'test_data'
    driver = 'Romain Grosjean'
    print_driver_info(test_folder, 'asc', driver)
    captured = capsys.readouterr()
    expected_output = """Driver Romain Grosjean info:
\ttime_start: 12:05:14.511
\ttime_end: 12:06:27.441
\tname: Romain Grosjean
\tteam: HAAS FERRARI
\ttime_diff: 0:01:12.930000
\tvalid: Time entry is valid
"""
    assert captured.out == expected_output


def test_build_report() -> NoReturn:
    """
    Test the build_report function - racers dictionary length. Invalid data should be removed from fastest_racers dict
    """
    test_folder = Path(__file__).resolve().parent.parent / 'tests' / 'test_data'
    order = 'asc'
    racers, fastest_racers = build_report(test_folder, order)

    assert len(racers) == 3
    assert len(fastest_racers) == 2


if __name__ == '__main__':
    unittest.main()
