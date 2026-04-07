# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Removed
- Removed deprecated `.opencode/` directory and symbolic links to consolidate skill management.

### Changed
- Rewrote `README.md` with real GitHub clone URL, skills table, project structure diagram, and clearer section organization.
- Renamed source package directory from `src/gemini_skills/` to `src/agent/`.
- Updated `main.py` greeting from "Hello from geminiSkills!" to "Hello from aiSkills!".
- Renamed project from `Gemini Skills` to `AI Skills` across README, pyproject.toml, and uv.lock.
- Defined a clear project description in `pyproject.toml`.
- Moved and consolidated all agent skills from `.agent/skills/` to the new `.agents/skills/` directory.
- Updated internal symbolic links in `.opencode/skills/` to reflect the new directory structure.
- Refined `README.md` introductory paragraph and skills table to perfectly align with skill definitions.

### Added
- Created `vulnerability-scanner` skill to scan dependencies and source code for CVEs and security vulnerabilities in Python, JavaScript, and Terraform projects.
- Added Terraform-focused skills bundle from `hashicorp/agent-skills` (stacks, style-guide, test, refactor-module, search-import).
- `.opencode/` folder with symbolic links to all available skills for streamlined access.
- `json-to-pydantic` skill and examples to convert JSON snippets to structured Python Pydantic models.
- `readme-updater` skill to maintain updating logic for README.md.
- `changelog-tracker` skill to manage and track project changelogs.
- `code-reviewer` skill to review code changes for quality and conformities.
- `license-header-adder` skill to automatically append license headers.
- Initial Python project structure.
- Apache 2.0 license and header template.
- Added `uv.lock` to track dependencies.
- Added `.gitignore` to exclude local environments (`.venv`).

### Changed
- Updated `.gitignore` to manage `.opencode/` subdirectories and configuration files.
- Rewrote `README.md` with real GitHub clone URL, skills table, project structure diagram, and clearer section organization.

### Changed
- Updated `README.md` to formally document newly-added skills and instructions.
- Updated `README.md` with the project title.
- Renamed project from `customagent` to `Gemini Skills` for consistency.
- Renamed `git-commit-formatter` directory to follow the standard skill structure.
