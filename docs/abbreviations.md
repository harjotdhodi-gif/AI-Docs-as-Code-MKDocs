---
title: Abbreviations and glossary
description: Definitions of common documentation, AI, compliance, and workflow terms.
tags:
  - Reference
  - Terminology
---

# Abbreviations and glossary

This page provides visible definitions for abbreviations used throughout the documentation.

!!! info "Hover tooltips"
    On other pages, hover over supported abbreviations such as **AI**, **API**, **CI/CD**, **RAG**, and **SME** to see their definitions. The tooltip definitions are maintained in `includes/abbreviations.md`.

## Common abbreviations

| Abbreviation | Meaning | Typical use |
|---|---|---|
| AI | Artificial intelligence | Automated or assisted documentation analysis |
| API | Application programming interface | Connecting applications and services |
| CI/CD | Continuous integration and continuous delivery | Automated validation, build, and publishing workflows |
| GDPR | General Data Protection Regulation | European data-protection requirements |
| HIPAA | Health Insurance Portability and Accountability Act | United States healthcare-data requirements |
| PDPL | Personal Data Protection Law | Personal-data protection requirements, including the UAE framework |
| RAG | Retrieval-augmented generation | Supplying approved source content to an AI system before generation |
| SME | Subject-matter expert | A person who validates technical accuracy |

## Workflow terms

Docs-as-Code
: A documentation approach that uses text-based source files, version control, automated checks, reviews, and publishing pipelines.

Human review
: The final editorial or technical decision made by an authorised reviewer after automated checks complete.

Pull Request
: A proposed set of repository changes submitted for automated checks and human review before merge.

Vale
: A configurable prose linter used to identify terminology, spelling, grammar, and style-guide deviations.

## Example

An SME reviews the RAG source content after the CI/CD workflow completes its automated checks. The API integration can then publish the approved documentation.
