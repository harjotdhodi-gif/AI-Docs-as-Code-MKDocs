---
title: Configuration
description: Configure validation, review, and publishing options for Atlas.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - configuration
  - yaml
---

# Configuration

Atlas reads project settings from `atlas.yml` in the repository root. Commit the file so local and automated builds use the same rules.

## Minimal configuration

```yaml
project:
  name: Atlas Sample
  source_dir: docs
  output_dir: site

validation:
  fail_on: error
  check_links: true
  require_front_matter: true

review:
  human_approval_required: true
```

Validate the configuration after each change:

```bash
atlas config check
```

## Configuration keys

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `project.source_dir` | String | `docs` | Directory containing Markdown source files. |
| `project.output_dir` | String | `site` | Directory containing generated output. |
| `validation.fail_on` | String | `error` | Lowest severity that fails the build. |
| `validation.check_links` | Boolean | `true` | Checks local and external links. |
| `validation.require_front_matter` | Boolean | `false` | Requires YAML metadata in every page. |
| `review.human_approval_required` | Boolean | `true` | Blocks publishing until a reviewer approves. |

Allowed values for `validation.fail_on` are `info`, `warning`, `error`, and `never`.

## Environment-specific values

Use environment variables for secrets and deployment-specific values:

```yaml
publishing:
  target: github-pages
  repository: ${ATLAS_REPOSITORY}
  token: ${ATLAS_TOKEN}
```

Set the variables in the CI platform's secret store. Do not add tokens to `atlas.yml`, workflow logs, examples, or screenshots.

## Precedence

Atlas resolves settings in this order, from highest to lowest priority:

1. Command-line options
2. Environment variables
3. `atlas.yml`
4. Built-in defaults

For example, `atlas validate --fail-on warning` overrides `validation.fail_on` for one run.

!!! danger
    Never commit an actual API key. If a credential is exposed, revoke it immediately and remove it from the Git history according to your incident-response procedure.

Related information: [Security and governance](07-security-and-governance.md).
