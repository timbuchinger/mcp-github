"""Tool definitions for GitHub MCP server."""

import json
from typing import Any, Dict

from ..commands.create import CreateIssueCommand
from ..commands.get import GetIssuesCommand
from ..github import GitHubClient, GitHubError


def get_github_client() -> GitHubClient:
    """Get an authenticated GitHub client from environment variables.

    Returns:
        Authenticated GitHub client

    Raises:
        GitHubError: If GitHub token is not configured
    """
    import os

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise GitHubError("GITHUB_TOKEN environment variable not set")

    return GitHubClient(token)


def format_error(error: GitHubError) -> Dict[str, Any]:
    """Format a GitHub error for MCP response.

    Args:
        error: GitHub error to format

    Returns:
        Dictionary containing error details
    """
    return {
        "content": [
            {
                "type": "text",
                "text": str(error),
            }
        ],
        "isError": True,
    }


def get_issues(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool implementation for getting GitHub issues.

    Args:
        arguments: Tool arguments containing repository

    Returns:
        Tool response containing issues or error
    """
    try:
        repo = arguments.get("repo")
        if not repo:
            raise GitHubError("Repository not specified")

        client = get_github_client()
        command = GetIssuesCommand(client, repo)
        result = command.execute()

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2),
                }
            ],
        }
    except GitHubError as e:
        return format_error(e)


def create_issue(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool implementation for creating GitHub issues.

    Args:
        arguments: Tool arguments containing repository, title, and body

    Returns:
        Tool response containing created issue or error
    """
    try:
        repo = arguments.get("repo")
        title = arguments.get("title")
        body = arguments.get("body", "")

        if not repo:
            raise GitHubError("Repository not specified")
        if not title:
            raise GitHubError("Issue title not specified")

        client = get_github_client()
        command = CreateIssueCommand(client, repo, title, body)
        result = command.execute()

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2),
                }
            ],
        }
    except GitHubError as e:
        return format_error(e)
