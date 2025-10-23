"""Server state management for ChillMCP."""

import time
from dataclasses import dataclass

from domain import boss, stress


@dataclass
class ServerState:
    """Manages the state of the ChillMCP server."""

    stress_level: int
    boss_alert_level: int
    last_stress_update_time: float
    last_boss_cooldown_time: float
    boss_alertness: int  # CLI parameter: probability (0-100) of boss alert increasing
    boss_alertness_cooldown: int  # CLI parameter: cooldown period in seconds

    @classmethod
    def create(
        cls, boss_alertness: int = 50, boss_alertness_cooldown: int = 300
    ) -> "ServerState":
        """Create a new ServerState with default initial values."""
        current_time = time.time()
        return cls(
            stress_level=0,
            boss_alert_level=0,
            last_stress_update_time=current_time,
            last_boss_cooldown_time=current_time,
            boss_alertness=boss_alertness,
            boss_alertness_cooldown=boss_alertness_cooldown,
        )

    def update_state(self) -> None:
        """
        Update state based on elapsed time.

        - Increases stress level based on time elapsed since last update
        - Decreases boss alert level based on cooldown periods elapsed
        """
        current_time = time.time()

        # Update stress level
        stress_elapsed = current_time - self.last_stress_update_time
        self.stress_level = stress.calculate_stress_increase(self.stress_level, stress_elapsed)
        self.last_stress_update_time = current_time

        # Update boss alert level (cooldown)
        boss_elapsed = current_time - self.last_boss_cooldown_time
        new_boss_alert = boss.calculate_boss_alert_cooldown(
            self.boss_alert_level, boss_elapsed, self.boss_alertness_cooldown
        )

        # Only update timestamp if boss alert actually decreased
        if new_boss_alert < self.boss_alert_level:
            # Reset timer for remaining cooldown
            periods_elapsed = int(boss_elapsed / self.boss_alertness_cooldown)
            self.last_boss_cooldown_time += periods_elapsed * self.boss_alertness_cooldown

        self.boss_alert_level = new_boss_alert
