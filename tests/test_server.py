"""Tests for the MCP GitHub server implementation."""

import asyncio
from datetime import datetime
from io import StringIO
from unittest.mock import AsyncMock, Mock, PropertyMock, patch

import pytest
from mcp.shared.exceptions import McpError
from mcp.types import TextContent

from mcp_github.github import GitHubError
from mcp_github.server import (
    handle_call_tool,
    list_resource_templates,
    list_resources,
    list_tools,
    server,
)


@pytest.fixture
def mock_transport():
    """Create mock input/output streams for testing."""
    input_stream = StringIO()
    output_stream = StringIO()
    return input_stream, output_stream


@pytest.mark.asyncio
async def test_list_tools():
    """Test that list_tools returns the expected tool definitions."""
    tools = await list_tools()

    assert isinstance(tools, list)
    assert len(tools) == 2  # get_issues and create_issue

    # Verify get_issues tool
    get_issues = next(t for t in tools if t["name"] == "get_issues")
    assert get_issues["description"] == "Get list of issues from a GitHub repository"
    assert get_issues["inputSchema"]["required"] == ["repo"]

    # Verify create_issue tool
    create_issue = next(t for t in tools if t["name"] == "create_issue")
    assert create_issue["description"] == "Create a new issue in a GitHub repository"
    assert set(create_issue["inputSchema"]["required"]) == {"repo", "title"}


@pytest.mark.asyncio
async def test_list_resources():
    """Test that list_resources returns an empty list."""
    resources = await list_resources()
    assert isinstance(resources, list)
    assert len(resources) == 0


@pytest.mark.asyncio
async def test_list_resource_templates():
    """Test that list_resource_templates returns an empty list."""
    templates = await list_resource_templates()
    assert isinstance(templates, list)
    assert len(templates) == 0


@pytest.mark.asyncio
@patch("mcp_github.tools.get_github_client")
async def test_get_issues_tool(mock_get_github_client):
    """Test the get_issues tool with valid arguments."""
    # Create a mock GitHub client
    mock_client = Mock()
    # Create a mock Issue object
    mock_issue = Mock()
    type(mock_issue).number = PropertyMock(return_value=1)
    type(mock_issue).title = PropertyMock(return_value="Test Issue")
    type(mock_issue).body = PropertyMock(return_value="Test body")
    type(mock_issue).state = PropertyMock(return_value="open")
    type(mock_issue).created_at = PropertyMock(return_value=datetime(2025, 2, 18))
    type(mock_issue).updated_at = PropertyMock(return_value=datetime(2025, 2, 18))

    mock_client.get_issues.return_value = [mock_issue]
    mock_get_github_client.return_value = mock_client

    response = await handle_call_tool("get_issues", {"repo": "owner/repo"})

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].type == "text"
    assert "Test Issue" in response[0].text
    mock_client.get_issues.assert_called_once_with("owner/repo", "open", None)


@pytest.mark.asyncio
@patch("mcp_github.tools.get_github_client")
async def test_create_issue_tool(mock_get_github_client):
    """Test the create_issue tool with valid arguments."""
    # Create a mock GitHub client
    mock_client = Mock()
    # Create a mock Issue object
    mock_issue = Mock()
    type(mock_issue).number = PropertyMock(return_value=1)
    type(mock_issue).title = PropertyMock(return_value="Test Issue")
    type(mock_issue).body = PropertyMock(return_value="Test Description")
    type(mock_issue).state = PropertyMock(return_value="open")
    type(mock_issue).created_at = PropertyMock(return_value=datetime(2025, 2, 18))
    type(mock_issue).updated_at = PropertyMock(return_value=datetime(2025, 2, 18))

    mock_client.create_issue.return_value = mock_issue
    mock_get_github_client.return_value = mock_client

    response = await handle_call_tool(
        "create_issue",
        {
            "repo": "owner/repo",
            "title": "Test Issue",
            "body": "Test Description",
        },
    )

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].type == "text"
    mock_client.create_issue.assert_called_once_with(
        "owner/repo", "Test Issue", "Test Description"
    )


@pytest.mark.asyncio
async def test_invalid_tool_name():
    """Test that calling an invalid tool name raises an error."""
    with pytest.raises(McpError) as exc_info:
        await handle_call_tool("invalid_tool", {})
    assert "Unknown tool: invalid_tool" in str(exc_info.value)


@pytest.mark.asyncio
@patch("mcp_github.tools.get_github_client")
async def test_missing_required_arguments(mock_get_github_client):
    """Test that calling a tool with missing required arguments raises an error."""
    response = await handle_call_tool(
        "create_issue", {"body": "Missing required repo and title"}
    )
    assert len(response) == 1
    assert response[0].type == "text"
    assert "Repository not specified" in response[0].text


@pytest.mark.asyncio
@patch("mcp_github.tools.get_github_client")
async def test_null_arguments(mock_get_github_client):
    """Test that calling a tool with null arguments doesn't crash."""
    response = await handle_call_tool("get_issues", None)
    assert len(response) == 1
    assert response[0].type == "text"
    assert "Repository not specified" in response[0].text
