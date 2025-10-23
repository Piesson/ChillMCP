"""Advanced slacking tools for ChillMCP."""

import random
import time

from fastmcp import FastMCP

from domain import boss, stress
from lib.response import build_response_text
from state import ServerState


def register_advanced_tools(mcp: FastMCP, state: ServerState) -> None:
    """Register advanced slacking tools with the MCP server."""

    @mcp.tool()
    def bathroom_break() -> str:
        """Take a bathroom break and scroll through your phone."""
        # Update state with elapsed time
        state.update_state()

        # Check if boss alert should increase
        if boss.should_increase_boss_alert(state.boss_alertness):
            state.boss_alert_level = min(state.boss_alert_level + 1, 5)

        # Reduce stress
        reduction = random.randint(1, 100)
        state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

        # Apply delay if boss alert is at max
        if state.boss_alert_level == 5:
            time.sleep(20)

        # Build response
        activities = [
            "scrolling through social media",
            "playing mobile games",
            "browsing online shopping",
            "watching short videos",
            "reading news",
        ]
        activity = random.choice(activities)
        summary = f"Bathroom break with {activity}... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def coffee_mission() -> str:
        """Go on a 'coffee mission' - walk around the office."""
        # Update state with elapsed time
        state.update_state()

        # Check if boss alert should increase
        if boss.should_increase_boss_alert(state.boss_alertness):
            state.boss_alert_level = min(state.boss_alert_level + 1, 5)

        # Reduce stress
        reduction = random.randint(1, 100)
        state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

        # Apply delay if boss alert is at max
        if state.boss_alert_level == 5:
            time.sleep(20)

        # Build response
        routes = [
            "took the scenic route through all floors",
            "chatted with colleagues along the way",
            "checked out the vending machines",
            "visited the rooftop garden",
            "stopped by the lounge area",
        ]
        route = random.choice(routes)
        summary = f"Coffee mission: {route}... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def urgent_call() -> str:
        """Pretend to take an urgent call and step outside."""
        # Update state with elapsed time
        state.update_state()

        # Check if boss alert should increase
        if boss.should_increase_boss_alert(state.boss_alertness):
            state.boss_alert_level = min(state.boss_alert_level + 1, 5)

        # Reduce stress
        reduction = random.randint(1, 100)
        state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

        # Apply delay if boss alert is at max
        if state.boss_alert_level == 5:
            time.sleep(20)

        # Build response
        excuses = [
            "important family matter",
            "doctor's appointment confirmation",
            "bank security issue",
            "delivery coordination",
            "emergency home repair",
        ]
        excuse = random.choice(excuses)
        summary = f"Urgent call about '{excuse}'... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def deep_thinking() -> str:
        """Pretend to be deep in thought while zoning out."""
        # Update state with elapsed time
        state.update_state()

        # Check if boss alert should increase
        if boss.should_increase_boss_alert(state.boss_alertness):
            state.boss_alert_level = min(state.boss_alert_level + 1, 5)

        # Reduce stress
        reduction = random.randint(1, 100)
        state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

        # Apply delay if boss alert is at max
        if state.boss_alert_level == 5:
            time.sleep(20)

        # Build response
        thoughts = [
            "staring at the ceiling contemplating life",
            "gazing out the window at clouds",
            "pondering the meaning of code",
            "contemplating lunch options",
            "thinking about weekend plans",
        ]
        thought = random.choice(thoughts)
        summary = f"Deep thinking mode: {thought}... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def email_organizing() -> str:
        """Organize emails while actually browsing online."""
        # Update state with elapsed time
        state.update_state()

        # Check if boss alert should increase
        if boss.should_increase_boss_alert(state.boss_alertness):
            state.boss_alert_level = min(state.boss_alert_level + 1, 5)

        # Reduce stress
        reduction = random.randint(1, 100)
        state.stress_level = stress.apply_stress_reduction(state.stress_level, reduction)

        # Apply delay if boss alert is at max
        if state.boss_alert_level == 5:
            time.sleep(20)

        # Build response
        activities = [
            "online shopping for gadgets",
            "browsing travel deals",
            "checking out new restaurants",
            "reading tech blogs",
            "watching product reviews",
        ]
        activity = random.choice(activities)
        summary = (
            f"Email organizing session with {activity}... reduced stress by {reduction} points"
        )
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text
