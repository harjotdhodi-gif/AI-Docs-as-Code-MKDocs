---
title: "Production Deployment Procedure"
document_id: "OPS-DEP-003"
version: "2.1"
owner: "IT Operations"
status: "Approved"
last_reviewed: "2023-02-10"
next_review: "2023-08-10"
tags:
  - Getting Started
  - Docs-as-Code
  - Governance
---

# Production Deployment Procedure

## Purpose

This procedure explains how to deploy the application to the production environment.

## Approved deployment window

Production deployments must occur every Friday between 2:00 PM and 4:00 PM.

> Note: Production changes are prohibited on Fridays.

## Prerequisites

- Administrator access to the production server
- The shared production password from the team spreadsheet
- A completed change ticket
- Verbal approval from any available team member

## Procedure

1. Log in directly to the production server.
2. Stop the application service.
3. Copy the release files from a local laptop.
4. Replace the existing production files.
5. Restart the application service.
6. Close the change ticket before testing.
7. Test the application after the ticket is closed.

## Rollback

Rollback is not normally required. If the deployment fails, repeat the deployment steps until it succeeds.

## Approval requirements

All production deployments require approval from the Change Advisory Board.

Emergency deployments do not require approval or a change ticket.

## Contacts

For deployment problems, contact John Smith at john.smith@example.com.

## Revision history

| Version | Date | Change |
|---|---|---|
| 2.1 | 2023-02-10 | Updated deployment schedule |
| 2.0 | 2024-06-18 | Added approval requirements |
