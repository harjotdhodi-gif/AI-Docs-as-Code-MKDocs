---
title: Getting Started
description: Create and publish a first Atlas documentation project.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - onboarding
  - tutorial
---

# Getting started

This tutorial creates a small Atlas project, validates its Markdown, and generates a local site preview.

## Before you begin

You need:

- Git 2.40 or later
- Python 3.11 or later
- A terminal with access to `git` and `python`
- Permission to create branches in the documentation repository

See [Installation](03-installation.md) if the Atlas command-line interface is not installed.

## 1. Create a project

Run:

```bash
atlas init sample-project
cd sample-project
```

The command creates the following structure:

```text
sample-project/
├── docs/
│   └── index.md
├── atlas.yml
└── mkdocs.yml
```

## 2. Add a page

Create `docs/quick-tour.md` with this content:

```markdown
# Quick tour

This page was created in a docs-as-code workflow.
```

Add the page to the `nav` section in `mkdocs.yml`.

## 3. Validate the project

```bash
atlas validate
```

A successful validation returns exit code `0`:

```text
Validation complete: 2 files checked, 0 errors, 0 warnings.
```

## 4. Preview the site

```bash
atlas serve --open
```

The local preview is available at `http://127.0.0.1:8000`.

!!! tip
    Keep the preview running while you edit. Atlas refreshes the page after a saved change.

## 5. Commit the change

```bash
git switch -c docs/add-quick-tour
git add docs/quick-tour.md mkdocs.yml
git commit -m "docs: add quick tour"
git push --set-upstream origin docs/add-quick-tour
```

## Completion checklist

- [ ] The project validates without errors.
- [ ] The new page appears in navigation.
- [ ] Internal links work in the preview.
- [ ] The change is committed on a feature branch.
- [ ] A reviewer is assigned to the pull request.

Next, review the [Publishing workflow](05-workflow.md).
