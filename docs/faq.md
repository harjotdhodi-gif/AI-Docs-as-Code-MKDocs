---
title: Frequently Asked Questions
description: Answers to common questions about Atlas and its documentation workflow.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - faq
  - support
---

# Frequently asked questions on Atlas Engine

## What is Atlas?

Atlas is a fictional command-line and API service used to demonstrate a governed docs-as-code workflow. It validates Markdown and supports automated publishing examples.

## Can I use these files with MkDocs Material?

Yes. Place the files in the MkDocs `docs/` directory and add them to the `nav` section of `mkdocs.yml`. Enable the `admonition` extension to render the callout blocks.

```yaml
markdown_extensions:
  - admonition
  - attr_list
  - tables
```

## Why does every page contain front matter?

Front matter provides structured metadata for ownership, lifecycle, search, reporting, and AI ingestion. The sample includes title, description, author, status, version, review date, and tags.

## Does AI approve documentation?

No. AI may identify issues or suggest changes, but an authorized human reviewer makes the final editorial and technical decision. See [Security and governance](07-security-and-governance.md).

## What should fail a pull request?

The organization must define its policy. Common blocking conditions include invalid Markdown, a failed strict build, broken internal links, exposed secrets, missing mandatory metadata, and unresolved high-risk findings.

## Can warnings be nonblocking?

Yes. Set a severity threshold in the validation configuration. For example, `fail_on: error` reports warnings but fails only on errors. Do not lower a threshold solely to make a failing check appear successful; correct the content or document an approved exception.

## How are PDF and Word files generated?

A pipeline can convert each Markdown page with tools such as Pandoc, then publish the generated files with the website. Generated files should identify the source commit to support traceability.

## Where should API keys be stored?

Store keys in the CI platform's encrypted secret store. Reference them through environment variables. Never commit actual keys to the repository.

## How often should a page be reviewed?

Set the interval according to risk and change frequency. Review security-sensitive or regulatory instructions more often than stable conceptual content. The `last_reviewed` field supports automated reminders.

## Where do I report a problem?

Follow the repository's issue template. Include reproduction steps and sanitized logs. For diagnostic guidance, see [Troubleshooting](08-troubleshooting.md).
