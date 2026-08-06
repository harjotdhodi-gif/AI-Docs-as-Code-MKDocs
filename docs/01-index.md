---
title: Atlas Documentation
description: Landing page for the Atlas sample documentation set.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - overview
  - sample
---

# Atlas Documentation

Welcome to the sample documentation for **Atlas**, a fictional service that helps teams organize, review, and publish technical content. This ten-page set is designed for testing a docs-as-code workflow with Markdown, GitHub, Vale, MkDocs Material, automated review, and human approval.

## What this sample tests

- YAML front matter and metadata validation
- Heading hierarchy and internal links
- Ordered, unordered, and task lists
- Tables, blockquotes, and inline formatting
- Shell, YAML, JSON, Python, and HTTP code blocks
- MkDocs Material admonitions
- API documentation and error handling
- Governance, security, FAQs, and release notes

## Documentation map

| Page | Purpose |
| --- | --- |
| [Getting started](02-getting-started.md) | Complete a five-minute product walkthrough. |
| [Installation](03-installation.md) | Install the command-line interface. |
| [Configuration](04-configuration.md) | Configure a project with YAML. |
| [Publishing workflow](05-workflow.md) | Review, approve, and publish changes. |
| [API reference](06-api-reference.md) | Test endpoint and payload documentation. |
| [Security and governance](07-security-and-governance.md) | Apply access, review, and retention controls. |
| [Troubleshooting](08-troubleshooting.md) | Resolve common errors. |
| [Frequently asked questions](09-faq.md) | Find concise answers. |
| [Release notes](10-release-notes.md) | Review changes by version. |

!!! note
    Atlas is fictional. Commands, URLs, credentials, and outputs in these files are safe examples and do not connect to a production system.

## Suggested test path

1. Add all files to a feature branch.
2. Modify one heading and one configuration value.
3. Open a pull request.
4. Confirm that style, link, build, and AI-review checks run.
5. Approve the pull request and verify the published site.

Continue with [Getting started](02-getting-started.md).
