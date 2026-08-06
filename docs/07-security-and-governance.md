---
title: Security and Governance
description: Security, access, review, retention, and AI-governance controls for Atlas documentation.
author: Governance Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - security
  - governance
  - ai
---

# Security and governance

Atlas documentation is governed as production content. Controls apply to source files, review records, generated output, secrets, and AI-assisted processing.

## Roles and responsibilities

| Role | Responsibility | Cannot do alone |
| --- | --- | --- |
| Author | Drafts and validates a change. | Approve a personally authored high-risk change. |
| Technical reviewer | Confirms technical accuracy. | Override security policy. |
| Editorial reviewer | Confirms clarity, style, and terminology. | Validate a system behavior without evidence. |
| Repository maintainer | Manages branches, checks, and releases. | Bypass required approvals. |
| Security owner | Approves security-sensitive guidance. | Publish directly to production. |

## Access controls

Apply least privilege to the repository and publishing platform:

- Require multifactor authentication for contributors.
- Protect the default branch from direct pushes and force pushes.
- Require at least one independent approval.
- Require status checks to pass before merge.
- Restrict workflow and secret-management changes to designated maintainers.
- Review access every quarter and after role changes.

## Content classification

| Classification | Example | Public documentation allowed? |
| --- | --- | --- |
| Public | Published product instructions | Yes |
| Internal | Draft roadmap or internal process | No |
| Confidential | Customer configuration or contract details | No |
| Restricted | Password, token, private key, regulated personal data | Never |

If content is classified above Public, keep it out of a public repository and use an approved private system.

## AI-assisted review controls

Before sending content to an external model:

1. Confirm that the model and data region are approved.
2. Remove secrets, personal data, customer identifiers, and unpublished confidential information.
3. Send only the minimum text needed for the review.
4. Record the model, prompt version, time, and result identifier.
5. Require a human to accept, reject, or revise each material recommendation.

> AI-generated feedback is advisory. Accountability remains with the authorized human approver.

## Retention and audit trail

Retain pull-request discussions, approvals, workflow logs, and release tags according to the organization's retention schedule. A release record should identify the source commit and deployed artifact.

!!! warning
    Never paste actual secrets into an issue, pull request, AI prompt, screenshot, or support ticket. Revoke an exposed secret before beginning cleanup.

Follow the [Publishing workflow](05-workflow.md) for approval gates.
