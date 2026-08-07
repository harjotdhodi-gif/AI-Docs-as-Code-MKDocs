---
title: API Reference
description: Reference for the sample Atlas document validation endpoint.
author: API Documentation Team
status: published
version: 1.2.0
last_reviewed: 2026-08-06
tags:
  - api
  - reference
---

# API reference

The Atlas API validates Markdown content and returns structured findings. The sample base URL is:

```text
https://api.example.com/v1
```

## Authentication

Send a bearer token in the `Authorization` header:

```http
Authorization: Bearer <token>
```

Store the token in a secret manager. Do not place it in source files.

## Validate a document

`POST /documents/validate`

Validates one UTF-8 Markdown document.

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | String | Yes | File name, including the `.md` extension. |
| `content` | String | Yes | Markdown content to validate. |
| `profile` | String | No | Rule profile. Default: `standard`. |
| `fail_on` | String | No | Minimum blocking severity. Default: `error`. |

### Example request

```bash
curl --request POST \
  --url https://api.example.com/v1/documents/validate \
  --header "Authorization: Bearer $ATLAS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "quick-tour.md",
    "content": "# Quick tour\\n\\nWelcome to Atlas.",
    "profile": "standard",
    "fail_on": "error"
  }'
```

### Successful response

Status: `200 OK`

```json
{
  "request_id": "req_01JATLAS9X2",
  "valid": true,
  "summary": {
    "errors": 0,
    "warnings": 1,
    "information": 0
  },
  "findings": [
    {
      "rule": "Atlas.Terms",
      "severity": "warning",
      "line": 3,
      "message": "Define the product name on first use."
    }
  ]
}
```

## Error responses

| Status | Code | Meaning |
| ---: | --- | --- |
| `400` | `invalid_request` | A required field is missing or malformed. |
| `401` | `unauthorized` | The token is missing, expired, or invalid. |
| `413` | `content_too_large` | The document exceeds the 1 MB limit. |
| `429` | `rate_limit_exceeded` | The client sent too many requests. |
| `500` | `internal_error` | The service could not complete validation. |

The API returns a request ID with every response. Include this ID when contacting support, but do not include the bearer token or document content.

See [Troubleshooting](08-troubleshooting.md) for retry guidance.
