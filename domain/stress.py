"""Stress management domain logic."""


def calculate_stress_increase(current_stress: int, elapsed_seconds: float) -> int:
    """
    Calculate new stress level based on elapsed time.

    Stress increases at 1 point per minute (60 seconds).

    Args:
        current_stress: Current stress level (0-100)
        elapsed_seconds: Time elapsed since last update in seconds

    Returns:
        New stress level capped at 100
    """
    # Calculate stress increase: 1 point per 60 seconds
    stress_increase = int(elapsed_seconds / 60.0)
    new_stress = current_stress + stress_increase

    # Cap at maximum 100
    return min(new_stress, 100)


def apply_stress_reduction(current_stress: int, reduction: int) -> int:
    """
    Apply stress reduction, ensuring it doesn't go below 0.

    Args:
        current_stress: Current stress level (0-100)
        reduction: Amount to reduce stress by

    Returns:
        New stress level with minimum of 0
    """
    new_stress = current_stress - reduction

    # Ensure minimum is 0
    return max(new_stress, 0)
