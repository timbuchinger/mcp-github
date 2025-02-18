"""Command for creating GitHub issues."""

from typing import Any, Dict

from github.Issue import Issue

from ..github import GitHubClient
from . import IssueCommand


class CreateIssueCommand(IssueCommand):
    """Command for creating a new issue in a GitHub repository."""

    def __init__(self, github_client: GitHubClient, repo: str, title: str, body: str):
        """Initialize command.

        Args:
            github_client: Authenticated GitHub client
            repo: Repository name in format "owner/repo"
            title: Issue title
            body: Issue body/description
        """
        self.github_client = github_client
        self.repo = repo
        self.title = title
        self.body = body

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
        """Execute the create issue command.

        Returns:
            Dictionary containing created issue data

        Raises:
            GitHubError: If there is an error creating the issue
        """
        issue = self.github_client.create_issue(self.repo, self.title, self.body)
        return {"issue": self._format_issue(issue)}
