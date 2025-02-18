"""MCP server implementation for GitHub integration."""

from typing import Dict

from modelcontextprotocol.sdk import Server
from modelcontextprotocol.sdk.server import StdioServerTransport
from modelcontextprotocol.sdk.types import CallToolRequestSchema, ListToolsRequestSchema

from .tools import create_issue, get_issues


class GitHubMCPServer:
    """MCP server for GitHub integration."""

    def __init__(self):
        """Initialize the GitHub MCP server."""
        self.server = Server(
            {
                "name": "github",
                "version": "0.1.0",
            },
            {
                "capabilities": {
                    "tools": {},
                }
            },
        )

        self._setup_handlers()
        self.server.onerror = lambda error: print("[MCP Error]", error)

    def _setup_handlers(self):
        """Set up request handlers for MCP server."""
        self.server.setRequestHandler(
            ListToolsRequestSchema,
            lambda _: {
                "tools": [
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
            },
        )

        tool_handlers: Dict[str, callable] = {
            "get_issues": get_issues,
            "create_issue": create_issue,
        }

        def handle_tool_call(request):
            handler = tool_handlers.get(request.params.name)
            if not handler:
                raise ValueError(f"Unknown tool: {request.params.name}")
            return handler(request.params.arguments)

        self.server.setRequestHandler(CallToolRequestSchema, handle_tool_call)

    async def run(self):
        """Run the MCP server on stdio transport."""
        transport = StdioServerTransport()
        await self.server.connect(transport)


def main():
    """Run the GitHub MCP server."""
    import asyncio

    server = GitHubMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
