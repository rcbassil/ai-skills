---
name: changelog-tracker
description: Manages and tracks changelogs in the project following the "Keep a Changelog" format. Use this when the user asks to update the changelog, document changes for a release, or track unreleased modifications.
---

# Changelog Tracker Skill

When asked to update the project documentation or track changes, you MUST maintain a `CHANGELOG.md` file following the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

## Format

The changelog should be a `CHANGELOG.md` file located at the root of the project. It tracks changes grouped by version and categorizes them clearly.

### Categories
For each given version, group the changes into one of the following headings:
- **Added**: for new features.
- **Changed**: for changes in existing functionality.
- **Deprecated**: for soon-to-be removed features.
- **Removed**: for now removed features.
- **Fixed**: for any bug fixes.
- **Security**: in case of vulnerabilities.

## Instructions

1. **Verify File**: Check if a `CHANGELOG.md` file exists in the root directory. If not, create it with a `# Changelog` heading and introductory text.
2. **Find Unreleased Section**: Look for the `## [Unreleased]` heading. If it doesn't exist, create it at the top of the version history.
3. **Determine Category**: Decide which of the allowed categories (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`) best fits the new changes.
4. **Log the Change**: Append a precise, one-line description of the change as a bullet point under the appropriate category heading within the `## [Unreleased]` section.
5. **Release Management**: If the user requests to draft a new release, rename the `## [Unreleased]` heading to include the new version number and the current date in ISO format (`YYYY-MM-DD`). For example: `## [1.0.0] - 2026-04-05`. Then, create a new empty `## [Unreleased]` section at the top.

## Example

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Implemented user authentication with JWT.
- Added user profile page.

### Fixed
- Resolved timezone offset issue in date picker.

## [1.0.0] - 2026-03-10

### Added
- Initial release of the application.
```
