---
title: Troubleshooting
description: Diagnose and resolve common Atlas installation, validation, build, and API errors.
author: Support Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - troubleshooting
  - support
---

# Troubleshooting

Start with the diagnostic command:

```bash
atlas doctor --verbose
```

Remove secrets and personal data before sharing diagnostic output.

## `atlas: command not found`

**Cause:** The executable directory is not in the shell path, or the virtual environment is inactive.

**Resolution:**

1. Run `pipx list` and confirm that `atlas-docs` is installed.
2. Run `python -m pipx ensurepath`.
3. Restart the terminal.
4. If using a virtual environment, activate it and try again.

See [Installation](03-installation.md) for platform-specific activation commands.

## Configuration file not found

**Message:**

```text
ATLAS-CFG-001: atlas.yml was not found.
```

**Resolution:** Run the command from the repository root or pass an explicit path:

```bash
atlas validate --config ./config/atlas.yml
```

## Strict build fails on a warning

A strict MkDocs build treats warnings as failures. Read the first warning in the log; later errors may be consequences of the same issue.

Common causes include:

- A navigation entry points to a missing file.
- An internal link uses the wrong relative path.
- A page is present in `docs/` but absent from navigation.
- A Markdown extension is used but not enabled.

Run:

```bash
mkdocs build --strict --verbose
```

## API returns `401 unauthorized`

Confirm that the token exists without printing its value:

```bash
test -n "$ATLAS_TOKEN" && echo "Token is set" || echo "Token is missing"
```

If the token is present, verify its expiry and scope in the approved secret-management system. Rotate the token if exposure is suspected.

## API returns `429 rate_limit_exceeded`

Honor the `Retry-After` response header. Use exponential backoff with jitter and a maximum retry count.

```python
import random
import time

for attempt in range(1, 5):
    delay = min(2 ** attempt, 30) + random.random()
    time.sleep(delay)
```

Do not retry `400` or `401` responses without correcting the request or credential.

## Information to include in a support request

- Atlas version
- Operating system and Python version
- Exact command, with secret values removed
- Full error message and request ID
- Minimal steps to reproduce the problem

For concise product answers, see the [Frequently asked questions](09-faq.md).
