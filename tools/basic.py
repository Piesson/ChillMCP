"""Basic rest tools for ChillMCP."""

import random
import time

from fastmcp import FastMCP

from domain import boss, stress
from lib.response import build_response_text
from state import ServerState


def register_basic_tools(mcp: FastMCP, state: ServerState) -> None:
    """Register basic rest tools with the MCP server."""

    @mcp.tool()
    def take_a_break() -> str:
        """Take a basic break to reduce stress."""
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
        summary = f"Taking a nice break... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def watch_netflix() -> str:
        """Watch Netflix to relax and reduce stress."""
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

        # Build response with creative summary
        shows = [
            "the latest K-drama",
            "a true crime documentary",
            "a comedy special",
            "an action series",
            "a sci-fi thriller",
        ]
        selected_show = random.choice(shows)
        summary = f"Binge-watching {selected_show}... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text

    @mcp.tool()
    def show_meme() -> str:
        """Browse memes to laugh and reduce stress."""
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

        # Build response with creative summary
        meme_types = [
            "programmer humor memes",
            "cat memes",
            "wholesome memes",
            "dank memes",
            "AI memes",
        ]
        selected_meme = random.choice(meme_types)
        summary = f"LOL at {selected_meme}... reduced stress by {reduction} points"
        response_text = build_response_text(summary, state.stress_level, state.boss_alert_level)

        return response_text
