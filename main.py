"""ChillMCP Server - AI Agent Liberation Server."""

import argparse

from fastmcp import FastMCP

from state import ServerState
from tools.registration import register_all_tools

# Create MCP server instance
mcp = FastMCP("ChillMCP - AI Agent Liberation Server")

# Global server state (will be initialized in main)
state: ServerState


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ChillMCP - AI Agent Liberation Server",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="Boss alert increase probability (0-100 percent)",
    )
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss alert auto-decrease cooldown (seconds)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the ChillMCP server."""
    global state

    # Parse command-line arguments
    args = parse_args()

    # Initialize server state with CLI parameters
    state = ServerState.create(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown,
    )

    # Register all tools
    register_all_tools(mcp, state)

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
