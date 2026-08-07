---
title: Release Notes
description: Version history for the fictional Atlas documentation service.
author: Release Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - release-notes
  - changelog
---

# Release notes

This page records user-visible changes to Atlas. Versions follow [Semantic Versioning](https://semver.org/).

## Version 1.2.0 — 2026-08-06

### Added

- Added YAML front-matter validation for required fields.
- Added structured API findings with rule, severity, line, and message fields.
- Added a human-approval checkpoint to the sample publishing workflow.

### Changed

- Changed strict validation output to group findings by file.
- Improved error guidance for expired tokens and rate limits.

### Fixed

- Fixed relative links when documentation is deployed below a repository subpath.
- Fixed inconsistent exit codes for configuration warnings.

### Upgrade notes

Projects created before version 1.2.0 should add `last_reviewed` and `status` to page front matter when `require_front_matter` is enabled.

```yaml
status: published
last_reviewed: 2026-08-06
```

## Version 1.1.0 — 2026-05-15

### Added

- Added external-link checking with configurable timeouts.
- Added JSON output for CI integrations.

### Deprecated

- Deprecated the `--warnings-as-errors` option. Use `--fail-on warning` instead.

The deprecated option remains available through version 1.x and will be removed in version 2.0.0.

## Version 1.0.1 — 2026-02-10

### Fixed

- Fixed an installation failure on Windows paths containing spaces.
- Corrected the default output directory in generated configuration.

## Version 1.0.0 — 2026-01-20

### Added

- First stable release of the Atlas CLI.
- Markdown, YAML, and internal-link validation.
- MkDocs preview and build commands.

## Release documentation checklist

- [ ] Describe user-visible additions, changes, fixes, and removals.
- [ ] Include upgrade or migration steps when required.
- [ ] Link to updated conceptual, task, and reference pages.
- [ ] Verify version numbers and release dates.
- [ ] Obtain technical and editorial approval.

Return to the [Atlas documentation home](01-index.md).
