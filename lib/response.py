"""Response formatting utilities for ChillMCP server."""


def build_response_text(summary: str, stress_level: int, boss_alert_level: int) -> str:
    """
    Build a response text that conforms to the parseable format required by the spec.

    Args:
        summary: Break activity summary
        stress_level: Current stress level (0-100)
        boss_alert_level: Current boss alert level (0-5)

    Returns:
        Formatted response string that can be parsed by regex patterns
    """
    return f"""Break Summary: {summary}
Stress Level: {stress_level}
Boss Alert Level: {boss_alert_level}"""
