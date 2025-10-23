"""Boss alert management domain logic."""

import random


def should_increase_boss_alert(boss_alertness: int) -> bool:
    """
    Determine if boss alert should increase based on probability.

    Args:
        boss_alertness: Probability (0-100) that boss alert increases

    Returns:
        True if boss alert should increase, False otherwise
    """
    # Generate random number from 0 to 99
    # If random number is less than boss_alertness, increase alert
    return random.randint(0, 99) < boss_alertness


def calculate_boss_alert_cooldown(
    current_alert: int, elapsed_seconds: float, cooldown_period: int
) -> int:
    """
    Calculate new boss alert level based on cooldown period.

    Boss alert decreases by 1 for every cooldown period that has elapsed.

    Args:
        current_alert: Current boss alert level (0-5)
        elapsed_seconds: Time elapsed since last cooldown in seconds
        cooldown_period: Period in seconds for each 1-point decrease

    Returns:
        New boss alert level with minimum of 0
    """
    # Calculate how many cooldown periods have elapsed
    periods_elapsed = int(elapsed_seconds / cooldown_period)
    new_alert = current_alert - periods_elapsed

    # Ensure minimum is 0
    return max(new_alert, 0)
