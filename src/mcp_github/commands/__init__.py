"""Command implementations for GitHub operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class IssueCommand(ABC):
    """Base class for GitHub issue-related commands."""

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the command.

        Returns:
            Dict containing the command result

        Raises:
            GitHubError: If there is an error executing the command
        """
        pass
