"""Tests for stress management domain logic."""


from domain.stress import apply_stress_reduction, calculate_stress_increase


def test_calculate_stress_increase_over_time() -> None:
    """Test that stress increases at 1 point per minute."""
    initial_stress = 10

    # Test 1 minute (60 seconds)
    result = calculate_stress_increase(initial_stress, 60.0)
    assert result == 11, "Stress should increase by 1 after 60 seconds"

    # Test 5 minutes (300 seconds)
    result = calculate_stress_increase(initial_stress, 300.0)
    assert result == 15, "Stress should increase by 5 after 300 seconds"

    # Test 30 seconds (should be 0.5, rounded down to 0)
    result = calculate_stress_increase(initial_stress, 30.0)
    assert result == 10, "Stress should not increase for less than 60 seconds"

    # Test 90 seconds (1.5 minutes)
    result = calculate_stress_increase(initial_stress, 90.0)
    assert result == 11, "Stress should increase by 1 after 90 seconds"


def test_calculate_stress_increase_max_cap() -> None:
    """Test that stress cannot exceed 100."""
    initial_stress = 98

    # Should cap at 100
    result = calculate_stress_increase(initial_stress, 180.0)  # +3 would be 101
    assert result == 100, "Stress should cap at 100"

    # Already at max
    result = calculate_stress_increase(100, 60.0)
    assert result == 100, "Stress should stay at 100 when already maxed"


def test_apply_stress_reduction() -> None:
    """Test stress reduction with minimum boundary."""
    # Normal reduction
    result = apply_stress_reduction(50, 20)
    assert result == 30, "Stress should decrease by reduction amount"

    # Exact to zero
    result = apply_stress_reduction(50, 50)
    assert result == 0, "Stress should reach exactly 0"

    # Over-reduction should not go negative
    result = apply_stress_reduction(50, 75)
    assert result == 0, "Stress should not go below 0"

    # Already at zero
    result = apply_stress_reduction(0, 10)
    assert result == 0, "Stress should stay at 0"
