# AI Skills

A curated collection of reusable agent skills for the `.agent/skills` framework. These focused capabilities — from formatting commit messages to generating Pydantic models — can be invoked on demand by an AI coding assistant inside any workspace.

## Included Skills

| Skill | Description |
|---|---|
| **changelog-tracker** | Manages and tracks changelogs in the project following the "Keep a Changelog" format. |
| **code-reviewer** | Reviews code changes for quality, readability, maintainability, and conformity to best practices. |
| **git-commit-formatter** | Formats git commit messages according to Conventional Commits specification. |
| **json-to-pydantic** | Converts JSON data snippets into Python Pydantic data models. |
| **license-header-adder** | Adds the standard open-source license header to new source files. |
| **readme-updater** | Updates the project's README.md with comprehensive, up-to-date documentation. |

## Prerequisites

- **Python** 3.13+
- [**uv**](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
git clone https://github.com/rcbassil/aiSkills.git
cd aiSkills

# Using uv (recommended)
uv sync

# Using pip
pip install .
```

## Running the Application

```bash
# Using uv
uv run main.py

# Using python directly
python main.py
```

Expected output:

```
Hello from aiSkills!
```

## Usage Examples

Skills are activated by communicating your intent to the agent inside your workspace. For example:

```text
"Update the README"            → triggers readme-updater
"Commit these changes"         → triggers git-commit-formatter
"Review my code"               → triggers code-reviewer
"Document project changes"     → triggers changelog-tracker
"Convert this JSON to a model" → triggers json-to-pydantic
```

## Project Structure

```
.
├── .agent/skills/       # Skill definitions (SKILL.md + resources per skill)
├── .opencode/           # Symbolic links to skills (for developer access)
├── src/agent/           # Python package source
├── tests/               # Test suite
├── docs/                # Documentation
├── main.py              # Entry point
├── pyproject.toml       # Project metadata & dependencies
├── CHANGELOG.md         # Project changelog
└── LICENSE              # Apache License 2.0
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
