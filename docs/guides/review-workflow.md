# Review workflow (Docs-as-Code)

This page explains how documentation changes move from draft to published output.

## Roles

- **Author:** writes or updates Markdown content.
- **Reviewer:** validates technical accuracy and clarity.
- **Approver:** final human gate for publishing.

## Workflow overview

1. Author creates a feature branch.
2. Author opens a Pull Request (PR).
3. Automated checks run:
   - Markdown/style lint
   - MkDocs build
   - Deviation Alert (LLM review of the diff)
4. Reviewer requests changes or approves.
5. After approval, the PR is merged.
6. Publishing workflow generates:
   - HTML site (GitHub Pages)
   - PDF exports
   - Word exports

## What the Deviation Alert checks

The LLM review focuses on:

- Meaning drift (did the change alter requirements or intent?)
- Grammar and vocabulary issues
- Consistency with our standards (Microsoft-style preferences + editorial consistency)
- Terminology mismatches

!!! warning
    The LLM report is advisory. A human reviewer must confirm technical accuracy before approval.

## Approval rules

A PR can be merged only when:

- Required CI checks pass
- At least one human reviewer approves

## Where to find outputs

After merge to `main`:

- HTML is served from GitHub Pages
- PDFs and DOCX files appear under the **Downloads** page in the site navigation
