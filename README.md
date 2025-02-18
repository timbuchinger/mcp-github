# GitHub MCP Server

A Model Context Protocol (MCP) server implementation for interacting with GitHub issues through Cline.

## Features

- List GitHub issues from a repository
- Create new GitHub issues
- Error handling and validation
- Secure authentication via environment variables

## Installation

1. Clone the repository:
```bash
git clone https://github.com/timbuchinger/mcp-github.git
cd mcp-github
```

2. Install dependencies with Poetry:
```bash
poetry install
```

3. Copy the environment template and configure your GitHub token:
```bash
cp .env.template .env
```

Edit `.env` and add your GitHub Personal Access Token:
```bash
GITHUB_TOKEN=your_token_here
```

To create a GitHub Personal Access Token:
1. Go to GitHub Settings -> Developer settings -> Personal access tokens
2. Generate a new token with `repo` scope
3. Copy the token and paste it in your `.env` file

## Usage

Run the MCP server:
```bash
poetry run python -m mcp_github.server
```

The server will start and expose two tools to Cline:

### get_issues
Get a list of issues from a GitHub repository:
```json
{
  "repo": "owner/repo"
}
```

### create_issue
Create a new issue in a GitHub repository:
```json
{
  "repo": "owner/repo",
  "title": "Issue title",
  "body": "Issue description"
}
```

## Error Handling

The server handles common errors:
- Missing GitHub token
- Invalid repository name
- Missing required parameters
- GitHub API errors

Error responses include descriptive messages to help troubleshoot issues.

## Development

The project uses Poetry for dependency management. To set up a development environment:

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .

# Type checking
poetry run mypy .
