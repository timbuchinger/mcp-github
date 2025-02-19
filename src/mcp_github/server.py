"""MCP server implementation for GitHub integration."""

import logging
import sys
from typing import Dict

import mcp.types as types
from mcp.server import Server
from mcp.shared.exceptions import McpError
from mcp.types import (
    INTERNAL_ERROR,
    CallToolRequestParams,
    ErrorData,
    ListToolsRequest,
    TextContent,
)

from .tools import create_issue, get_issues

# Initialize server at module level
server = Server("github")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("mcp_github")


# Set up request handlers
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        {
            "name": "get_issues",
            "description": "Get list of issues from a GitHub repository",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name in format owner/repo",
                    },
                },
                "required": ["repo"],
            },
        },
        {
            "name": "create_issue",
            "description": "Create a new issue in a GitHub repository",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "Repository name in format owner/repo",
                    },
                    "title": {
                        "type": "string",
                        "description": "Issue title",
                    },
                    "body": {
                        "type": "string",
                        "description": "Issue body/description",
                    },
                },
                "required": ["repo", "title"],
            },
        },
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool operations."""
    logger.info(f"Handling tool {name} with arguments {arguments}")
    if not arguments:
        arguments = {}

    try:
        tool_handlers: Dict[str, callable] = {
            "get_issues": get_issues,
            "create_issue": create_issue,
        }

        handler = tool_handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")

        result = await handler(arguments)
        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        logger.exception(e)
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Error handling tool {name}: {e}",
            )
        )


async def run_server():
    """Run the MCP server on stdio transport."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


def main():
    """Run the GitHub MCP server."""
    import asyncio

    logger.info("Starting GitHub MCP server")
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
