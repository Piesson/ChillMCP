"""Tests for response formatting utilities."""

import re

from lib.response import build_response_text


def test_build_response_format() -> None:
    """Test that build_response_text generates parseable output."""
    # Generate test response
    response = build_response_text("Coffee break with scrolling", 45, 3)

    # Define regex patterns from requirements
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

    # Test Break Summary parsing
    break_match = re.search(break_summary_pattern, response, re.MULTILINE)
    assert break_match is not None, "Break Summary not found"
    assert break_match.group(1) == "Coffee break with scrolling"

    # Test Stress Level parsing
    stress_match = re.search(stress_level_pattern, response)
    assert stress_match is not None, "Stress Level not found"
    assert int(stress_match.group(1)) == 45

    # Test Boss Alert Level parsing
    boss_match = re.search(boss_alert_pattern, response)
    assert boss_match is not None, "Boss Alert Level not found"
    assert int(boss_match.group(1)) == 3


def test_build_response_boundary_values() -> None:
    """Test response formatting with boundary values."""
    # Test minimum values
    response_min = build_response_text("Quick rest", 0, 0)
    assert "Stress Level: 0" in response_min
    assert "Boss Alert Level: 0" in response_min

    # Test maximum values
    response_max = build_response_text("Long break", 100, 5)
    assert "Stress Level: 100" in response_max
    assert "Boss Alert Level: 5" in response_max
