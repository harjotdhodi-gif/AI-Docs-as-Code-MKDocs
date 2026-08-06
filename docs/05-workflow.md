---
title: Publishing Workflow
description: Review and publish documentation through a governed pull-request workflow.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - workflow
  - github
  - governance
---

# Publishing workflow

All Atlas documentation changes move through a pull request. Automated checks provide fast feedback; an authorized human reviewer makes the final editorial and technical decision.

## Workflow stages

| Stage | Owner | Required evidence | Exit condition |
| --- | --- | --- | --- |
| Draft | Author | Source or SME input | Content is ready for review. |
| Automated review | CI pipeline | Build, style, link, and AI reports | Required checks pass. |
| Human review | Technical and editorial reviewers | Comments and approvals | Required approvals are recorded. |
| Merge | Repository maintainer | Protected-branch status | Pull request is merged. |
| Publish | CI pipeline | Deployment log | Site health check passes. |

## Create a documentation change

1. Create a short-lived branch from the current default branch.
2. Edit only the files needed for the requested change.
3. Run validation and preview commands locally.
4. Commit with a clear message, such as `docs: clarify token rotation`.
5. Open a pull request and complete its checklist.

```bash
git switch main
git pull --ff-only
git switch -c docs/clarify-token-rotation
atlas validate
git add docs/
git commit -m "docs: clarify token rotation"
git push --set-upstream origin docs/clarify-token-rotation
```

## Required automated checks

- Markdown and YAML syntax
- Vale style rules
- Internal link integrity
- MkDocs strict build
- Secret scanning
- AI-assisted review for omissions, unsupported claims, and risky language

AI review findings are recommendations unless an approved policy maps a finding to a blocking severity. AI must not approve or merge a change.

## Human review checklist

- [ ] Technical steps are correct and reproducible.
- [ ] Claims cite an approved source or named subject-matter expert.
- [ ] Security and privacy information is appropriate for the audience.
- [ ] Terminology follows the product glossary.
- [ ] Screenshots and examples contain no personal or secret data.
- [ ] Navigation and related links are updated.
- [ ] Release notes are included when user behavior changes.

!!! important
    A passing pipeline does not replace human approval. Repository protection must prevent direct publication from an unreviewed branch.

See [Security and governance](07-security-and-governance.md) for roles and retention requirements.
