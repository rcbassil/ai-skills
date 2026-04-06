# Gemini Skills

Gemini Skills is a Python project designed to provide and manage a suite of specialized agent skills via the `.agent/skills` framework. 

The currently included skills enhance your project workspace organically:
- **Changelog Tracker**: Standardizes and manages `CHANGELOG.md` updates.
- **Code Reviewer**: Automates detailed code reviews based on best practices.
- **Git Commit Formatter**: Generates compliant Conventional Commit logs.
- **JSON to Pydantic**: Converts raw JSON snippets directly into structured Python models.
- **License Header Adder**: Appends legal licensing text to top of new files.
- **README Updater**: Automatically handles maintaining this very documentation.

## Prerequisites

- **Python:** version 3.13 or higher.

To spin it up, clone the repository and use [uv](https://github.com/astral-sh/uv) or pip:

```bash
git clone <your-repo-url>
cd geminiSkills

# Using uv (recommended)
uv run main.py

# Using pip
pip install .
python main.py
```

The main execution points to a straightforward entry script. To run it locally:

```bash
# Using uv
uv run main.py

# Using python
python main.py
```

## Usage Examples & Commands

To test the main module output, you can use:

```bash
python main.py
# Output: Hello from geminiSkills!
```

To invoke any of the active skills, communicate your intent to the agent within the workspace context. For instance:
- *"update the README"*
- *"Commit these changes"*
- *"Please document project changes"*
- *"Review my code"*
- *"{ 'product': 'Widget' } Convert this JSON to a Pydantic model"*
