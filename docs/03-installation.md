---
title: Installation
description: Install and verify the Atlas command-line interface.
author: Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - installation
  - cli
---

# Installation

Install the Atlas command-line interface (CLI) in an isolated Python environment. Isolation prevents Atlas dependencies from conflicting with other projects.

## Supported platforms

| Platform | Minimum version | Status |
| --- | ---: | --- |
| Windows | Windows 11 | Supported |
| macOS | 13 | Supported |
| Ubuntu | 22.04 LTS | Supported |
| Other Linux distributions | — | Community tested |

## Install with `pipx`

`pipx` is the recommended installation method.

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install atlas-docs==1.2.0
```

Restart the terminal after `ensurepath` updates the executable path.

## Install in a virtual environment

Use this method for CI runners or project-specific installations:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install atlas-docs==1.2.0
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Verify the installation

```bash
atlas --version
```

Expected output:

```text
atlas-docs 1.2.0
```

Also run a diagnostic check:

```bash
atlas doctor
```

The check confirms the Python version, configuration path, Markdown parser, and Git availability.

!!! warning
    Do not install Atlas with administrator or root privileges. A privileged installation can create files that ordinary users cannot modify.

## Upgrade or uninstall

```bash
pipx upgrade atlas-docs
pipx uninstall atlas-docs
```

For proxy, certificate, or path failures, see [Troubleshooting](08-troubleshooting.md).
