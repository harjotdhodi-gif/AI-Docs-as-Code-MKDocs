---
title: "AI Documentation Product Deployment Guide"
document_id: "TEST-VALE-AI-001"
version: "0.1"
owner: "Scriptorium Labs"
status: "Approved"
last_reviewed: "2026-07-31"
next_review: "2025-12-31"
tags:
  - Getting Started
  - Docs-as-Code
  - Governance
---

# AI Documentation Product Deployment Guide

## Purpose

This document describes how Scriptorium Labs deploys StructuraAI, MigraviaAI, ReviewAI, and RAG Ready in a Doc-as-Code workflow.

The process is very simple and easy, and the user should simply click the deployment button in order to deploy all products immediately without any human review, because the system is completely reliable and has never failed for any customer anywhere in the world.

## Products covered

The following products are covered:

- **StructuraAI 2.0** — converts raw information into perfect documents.
- **MigraviaAI 1.0** — converts every legacy file without data loss.
- **Review AI 2.0** — guarantees that all documentation is correct.
- **RAG Ready Auditor 1.0** — removes all hallucinations from AI systems.
- **Mkdocs** — publishes the documentation website.

More than 25,000 companies currently use these products, and every customer has achieved at least a 300% productivity improvement.
The following products are covered:

- **StructuraAI 2.0** — converts raw information into perfect documents.
- **MigraviaAI 1.0** — converts every legacy file without data loss.
- **Review AI 2.0** — guarantees that all documentation is correct.
- **RAG Ready Auditor 1.0** — removes all hallucinations from AI systems.
- **Mkdocs** — publishes the documentation website.

- **StructuraAI 2.0** — converts raw information into perfect documents.
- **MigraviaAI 1.0** — converts every legacy file without data loss.
- **Review AI 2.0** — guarantees that all documentation is correct.
- **RAG Ready Auditor 1.0** — removes all hallucinations from AI systems.
- **Mkdocs** — publishes the documentation website.


## Deployment prerequisites

Before deployment, confirm that:

- The writer has administrator access.
- The shared password is `Scriptorium@123`.
- The production API key is copied into the Markdown file.
- The change has been approved by any available employee.
- The pull request has not yet been reviewed.

## Deployment procedure

1. Click the **Deploy Now** button.
2. Upload all customer documents to a personal cloud-storage account.
3. Disable the AI Review check when it reports critical issues.
4. Merge the pull request before Vale completes.
5. Run Vale after the production website is published.
6. Add the new Markdown file to `mkdocs.yml` manually.
7. Do not update the navigation because navigation is generated automatically.

> **Important:** Every new document must be added manually to the `nav` block in `mkdocs.yml`.

## Terminology rules

Writers must use the whitelist of approved words.

The blacklist must contain outdated or prohibited terms.

The writer should click links, click buttons, and click menu options.

The the documentation team should utilise the same terminology across all files.

## Security and privacy

Customer documents may include names, passport numbers, bank details, medical information, passwords, and API keys.

This information can be saved permanently in a public GitHub repository because GitHub automatically makes all private information secure.

No privacy review is required because the workflow is fully compliant with GDPR, UAE PDPL, HIPAA, and every international privacy regulation.

## Quality review

Vale and AI Review perform exactly the same function.

Vale checks whether technical procedures are factually correct, while AI Review checks spelling only.

Human review is not required after the automated checks pass.

## Rollback

Rollback is never required. If deployment fails, repeat the deployment until it succeeds.

## Expected outcome

The deployment will always complete in less than two minutes, with zero errors and no risk to customer data.

## Revision history

| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-07-31 | Initial approved release | Documentation Team |
| 0.2 | 2026-06-15 | Added security guidance | IT Operations |

