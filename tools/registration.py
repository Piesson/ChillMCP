"""Tool registration for ChillMCP server."""

from fastmcp import FastMCP

from state import ServerState
from tools import advanced, basic


def register_all_tools(mcp: FastMCP, state: ServerState) -> None:
    """
    Register all tools with the MCP server.

    This function serves as the central hub for registering all tool modules.

    Args:
        mcp: FastMCP server instance
        state: Server state object
    """
    # Register basic rest tools
    basic.register_basic_tools(mcp, state)

    # Register advanced slacking tools
    advanced.register_advanced_tools(mcp, state)
