"""Tests for boss alert management domain logic."""

from domain.boss import calculate_boss_alert_cooldown, should_increase_boss_alert


def test_should_increase_boss_alert_probability() -> None:
    """Test boss alert increase probability logic."""
    # Test 100% probability - should always return True
    results_100 = [should_increase_boss_alert(100) for _ in range(20)]
    assert all(results_100), "boss_alertness=100 should always increase alert"

    # Test 0% probability - should always return False
    results_0 = [should_increase_boss_alert(0) for _ in range(20)]
    assert not any(results_0), "boss_alertness=0 should never increase alert"

    # Test 50% probability - should have mix of True/False
    # Run 100 times to get statistical significance
    results_50 = [should_increase_boss_alert(50) for _ in range(100)]
    true_count = sum(results_50)
    # With 100 samples at 50%, we expect ~50 True values
    # Allow range of 30-70 to account for randomness
    assert 30 <= true_count <= 70, f"boss_alertness=50 should be ~50% True, got {true_count}/100"


def test_calculate_boss_alert_cooldown() -> None:
    """Test boss alert cooldown calculation."""
    initial_alert = 3
    cooldown_period = 300  # 5 minutes

    # Test 1 cooldown period (300 seconds)
    result = calculate_boss_alert_cooldown(initial_alert, 300.0, cooldown_period)
    assert result == 2, "Boss alert should decrease by 1 after 1 cooldown period"

    # Test 2 cooldown periods (600 seconds)
    result = calculate_boss_alert_cooldown(initial_alert, 600.0, cooldown_period)
    assert result == 1, "Boss alert should decrease by 2 after 2 cooldown periods"

    # Test less than 1 cooldown period
    result = calculate_boss_alert_cooldown(initial_alert, 150.0, cooldown_period)
    assert result == 3, "Boss alert should not decrease if less than cooldown period"

    # Test 1.5 cooldown periods (450 seconds) - should decrease by 1
    result = calculate_boss_alert_cooldown(initial_alert, 450.0, cooldown_period)
    assert result == 2, "Boss alert should decrease by 1 after 1.5 cooldown periods"


def test_calculate_boss_alert_cooldown_min_cap() -> None:
    """Test that boss alert cannot go below 0."""
    initial_alert = 2
    cooldown_period = 60  # 1 minute

    # Should decrease to 0, not negative
    result = calculate_boss_alert_cooldown(initial_alert, 180.0, cooldown_period)  # 3 periods
    assert result == 0, "Boss alert should cap at 0"

    # Already at 0
    result = calculate_boss_alert_cooldown(0, 60.0, cooldown_period)
    assert result == 0, "Boss alert should stay at 0"


def test_calculate_boss_alert_cooldown_short_period() -> None:
    """Test boss alert with short cooldown period (for testing)."""
    initial_alert = 5
    cooldown_period = 10  # 10 seconds

    # Test 10 seconds
    result = calculate_boss_alert_cooldown(initial_alert, 10.0, cooldown_period)
    assert result == 4, "Boss alert should decrease by 1 after 10 seconds"

    # Test 60 seconds (6 periods)
    result = calculate_boss_alert_cooldown(initial_alert, 60.0, cooldown_period)
    assert result == 0, "Boss alert should reach 0 after 60 seconds"
