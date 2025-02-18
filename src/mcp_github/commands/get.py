"""Command for retrieving GitHub issues."""

from typing import Any, Dict, List

from github.Issue import Issue

from ..github import GitHubClient
from . import IssueCommand


class GetIssuesCommand(IssueCommand):
    """Command for retrieving issues from a GitHub repository."""

    def __init__(self, github_client: GitHubClient, repo: str):
        """Initialize command.

        Args:
            github_client: Authenticated GitHub client
            repo: Repository name in format "owner/repo"
        """
        self.github_client = github_client
        self.repo = repo

    def _format_issue(self, issue: Issue) -> Dict[str, Any]:
        """Format a GitHub issue into a dictionary.

        Args:
            issue: GitHub issue to format

        Returns:
            Dictionary containing formatted issue data
        """
        return {
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
            "state": issue.state,
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.isoformat(),
        }

    def execute(self) -> Dict[str, Any]:
        """Execute the get issues command.

        Returns:
            Dictionary containing list of issues

        Raises:
            GitHubError: If there is an error retrieving the issues
        """
        issues = self.github_client.get_issues(self.repo)
        return {"issues": [self._format_issue(issue) for issue in issues]}
