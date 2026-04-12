# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `drawio-diagram` skill to generate native `.drawio` architecture diagrams, flowcharts, ER diagrams, sequence diagrams, and more — with optional export to PNG, SVG, and PDF.
- `aiSkills-architecture.drawio` — architecture overview diagram of the project.

### Changed
- Updated `README.md` skills table and usage examples to include `drawio-diagram`.

## [0.4.0] - 2026-04-12

### Removed
- Removed deprecated `.opencode/` directory and symbolic links to consolidate skill management.

### Changed
- Rewrote `README.md` with real GitHub clone URL, skills table, project structure diagram, and clearer section organization.
- Renamed source package directory from `src/gemini_skills/` to `src/agent/`.
- Updated `main.py` greeting from "Hello from geminiSkills!" to "Hello from aiSkills!".
- Renamed project from `Gemini Skills` to `AI Skills` across README, pyproject.toml, and uv.lock.
- Defined a clear project description in `pyproject.toml`.
- Moved and consolidated all agent skills from `.agent/skills/` to the new `.agents/skills/` directory.
- Refined `README.md` introductory paragraph and skills table to perfectly align with skill definitions.

### Added
- Created `kubernetes-troubleshooter` skill as a DevSecOps assistant for diagnosing issues within a Kubernetes cluster.
- Created `vulnerability-scanner` skill to scan dependencies and source code for CVEs and security vulnerabilities in Python, JavaScript, and Terraform projects.
- Added Terraform-focused skills bundle from `hashicorp/agent-skills` (stacks, style-guide, test, refactor-module, search-import).
- `json-to-pydantic` skill and examples to convert JSON snippets to structured Python Pydantic models.
- `readme-updater` skill to maintain updating logic for README.md.
- `changelog-tracker` skill to manage and track project changelogs.
- `code-reviewer` skill to review code changes for quality and conformities.
- `license-header-adder` skill to automatically append license headers.
- Initial Python project structure.
- Apache 2.0 license and header template.
- Added `uv.lock` to track dependencies.
- Added `.gitignore` to exclude local environments (`.venv`).
