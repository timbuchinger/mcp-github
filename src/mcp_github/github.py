"""GitHub API client implementation."""

from typing import List, Optional

from github import Github, GithubException
from github.Issue import Issue


class GitHubError(Exception):
    """Custom exception for GitHub API errors."""

    def __init__(self, message: str, status: Optional[int] = None):
        self.status = status
        super().__init__(message)


class GitHubClient:
    """Client for interacting with GitHub API."""

    def __init__(self, token: str):
        """Initialize GitHub client with authentication token.

        Args:
            token: GitHub personal access token
        """
        self.api = Github(token)

    def get_issues(
        self, repo: str, state: str = "open", query: Optional[str] = None
    ) -> List[Issue]:
        """Get list of issues from a repository.

        Args:
            repo: Repository name in format "owner/repo"
            state: State of issues to retrieve ("open", "closed", or "all")
            query: Optional search query to filter issues

        Returns:
            List of GitHub issues

        Raises:
            GitHubError: If there is an error accessing the issues
        """
        try:
            repository = self.api.get_repo(repo)
            if query:
                query_str = f"repo:{repo} {query} state:{state}"
                return list(self.api.search_issues(query_str))
            return list(repository.get_issues(state=state))
        except GithubException as e:
            raise GitHubError(str(e.data.get("message", "Unknown error")), e.status)

    def create_issue(self, repo: str, title: str, body: str) -> Issue:
        """Create a new issue in a repository.

        Args:
            repo: Repository name in format "owner/repo"
            title: Issue title
            body: Issue body/description

        Returns:
            Created GitHub issue

        Raises:
            GitHubError: If there is an error creating the issue
        """
        try:
            repository = self.api.get_repo(repo)
            return repository.create_issue(title=title, body=body)
        except GithubException as e:
            raise GitHubError(str(e.data.get("message", "Unknown error")), e.status)
