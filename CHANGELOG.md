# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `audio-transcriber` skill to transcribe audio and video files to `.srt` subtitle format with precise timestamps using faster-whisper. Processes audio in overlapping chunks with `initial_prompt` context passing to prevent vocabulary drift across boundaries. Supports all common formats (mp3, wav, m4a, flac, ogg, mp4) and all Whisper model sizes from `tiny` to `large-v3`.
- `kubernetes-readonly-troubleshooter` skill for diagnosing Kubernetes resources, logs, network routes, and RBAC in strict read-only mode — enforces zero cluster mutations.
- `token-compressor` skill to reduce token usage and AI agent costs by compressing prompts, context, and conversation history — with explicit quality-protection rules that prevent code blocks, few-shot examples, regex, and error messages from being altered. Includes a local LLM routing strategy (Ollama) for simple sub-tasks to achieve $0 cost on classify/summarize/format workloads.
- `drawio` skill to generate native `.drawio` architecture diagrams, flowcharts, ER diagrams, sequence diagrams, and more — with optional export to PNG, SVG, and PDF.
- `ai-skills-architecture.drawio` — architecture overview diagram of the project.

### Changed
- Renamed project folder and all references from `aiSkills` to `ai-skills` (kebab-case convention).
- Renamed `aiSkills-architecture.drawio` and `docs/aiSkills-architecture.drawio.png` to `ai-skills-*`.
- Updated `main.py` greeting, `README.md` clone URL, and diagram image reference to reflect new name.
- Updated `README.md` skills table and usage examples to include all new skills.

## [0.4.0] - 2026-04-12

### Removed
- Removed deprecated `.opencode/` directory and symbolic links to consolidate skill management.

### Changed
- Rewrote `README.md` with real GitHub clone URL, skills table, project structure diagram, and clearer section organization.
- Renamed source package directory from `src/gemini_skills/` to `src/agent/`.
- Updated `main.py` greeting from "Hello from geminiSkills!" to "Hello from ai-skills!".
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
