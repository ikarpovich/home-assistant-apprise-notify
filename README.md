# Home Assistant Apprise Notify

Home Assistant custom notify integration for sending notifications through an Apprise API server.

## Status

This repository is being built in small PRs. Current state:

- HACS-compatible repository scaffold.
- CI for linting and tests.
- HACS and Hassfest validation workflows.
- Dependabot for GitHub Actions and Python dependencies.

The notify platform implementation will be added in a follow-up PR.

## Planned usage

The integration will expose a Home Assistant notify service backed by an Apprise API endpoint, preserving Apprise features such as markdown formatting and attachments where supported by the downstream notification provider.
