import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI

REPORT_ONLY = os.getenv("AI_REVIEW_REPORT_ONLY", "0").lower() in ("1", "true", "yes")

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(
    os.getenv("AI_REVIEW_REPORT_PATH", str(REPO_ROOT / "ai-review-report.md"))
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
FAIL_ON_SEVERITY = os.getenv("FAIL_ON_SEVERITY", "critical").lower()
SEVERITY_ORDER = {"minor": 1, "major": 2, "critical": 3}

SYSTEM_RULES = """You are a senior technical editor and documentation QA reviewer.

Your job:
1) Identify content deviations: what materially changed and whether it introduced ambiguity, inconsistency, missing context, or factual risk.
2) Identify writing deviations: grammar, vocabulary, clarity, tone.
3) Enforce style guidance:
   - Microsoft Writing Style Guide (clarity, active voice, consistent terms, accessible language)
   - Chicago Manual of Style (punctuation consistency, headings consistency, basic editorial rigor)
4) Output a structured review with issues and suggested fixes.

Be precise, practical, and avoid rewriting everything. Flag only meaningful issues.
Return STRICT JSON only.
"""


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, cwd=str(REPO_ROOT), text=True).strip()


def get_changed_md_files() -> List[str]:
    base = os.getenv("GITHUB_BASE_SHA")
    head = os.getenv("GITHUB_HEAD_SHA")
    if not base or not head:
        base = "origin/main"
        head = "HEAD"

    output = run(["git", "diff", "--name-only", f"{base}...{head}"])
    files = [
        path
        for path in output.splitlines()
        if path.startswith("docs/") and path.endswith(".md")
    ]
    return [path for path in files if not path.endswith("docs/downloads.md")]


def get_diff_for_file(path: str) -> str:
    base = os.getenv("GITHUB_BASE_SHA") or "origin/main"
    head = os.getenv("GITHUB_HEAD_SHA") or "HEAD"
    return run(["git", "diff", f"{base}...{head}", "--", path])


def severity_at_least(severity: str, threshold: str) -> bool:
    return SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER.get(threshold, 2)


def annotate(issue: Dict[str, Any]) -> None:
    severity = issue.get("severity", "minor")
    level = "error" if severity == "critical" else "warning"
    file_name = issue.get("file", "")
    line = issue.get("line")
    message = issue.get("message", "Issue")
    suggestion = issue.get("suggestion", "")
    full_message = message if not suggestion else f"{message} | Suggestion: {suggestion}"

    if file_name and line:
        print(f"::{level} file={file_name},line={line}::{full_message}")
    elif file_name:
        print(f"::{level} file={file_name}::{full_message}")
    else:
        print(f"::{level}::{full_message}")


def markdown_cell(value: Any) -> str:
    text = str(value if value not in (None, "") else "—")
    return text.replace("\r", " ").replace("\n", " ").replace("|", "\\|")


def write_report(
    changed_files: List[str],
    file_results: List[Dict[str, Any]],
    all_issues: List[Dict[str, Any]],
    runtime_error: str = "",
) -> None:
    counts = {
        severity: sum(
            1 for issue in all_issues if issue.get("severity", "minor") == severity
        )
        for severity in ("critical", "major", "minor")
    }

    if runtime_error:
        status = "🔴 AI review could not complete"
    elif counts["critical"]:
        status = "🔴 Critical issues found — do not merge"
    elif counts["major"]:
        status = "🟠 Major issues require review"
    elif counts["minor"]:
        status = "🟡 Minor issues found"
    else:
        status = "✅ No AI review issues found"

    lines = [
        "# AI Documentation Review",
        "",
        f"**Status:** {status}",
        "",
        f"**Files reviewed:** {len(changed_files)}  ",
        f"**Critical:** {counts['critical']} · **Major:** {counts['major']} · **Minor:** {counts['minor']}",
        "",
        "> AI Review checks meaning, contradictions, unsupported claims, missing context, and operational or compliance risks. A human reviewer makes the final decision.",
        "",
    ]

    if changed_files:
        lines.extend(
            [
                "**Changed files:** "
                + ", ".join(f"`{path}`" for path in changed_files),
                "",
            ]
        )
    else:
        lines.extend(["No changed Markdown files were detected under `docs/`.", ""])

    if runtime_error:
        lines.extend(
            [
                "## Runtime error",
                "",
                "```text",
                runtime_error[:4000],
                "```",
                "",
            ]
        )

    for result in file_results:
        file_name = result.get("file", "Unknown file")
        summary = result.get("summary", "No summary returned.")
        issues = result.get("issues", [])

        lines.extend([f"## `{file_name}`", "", summary, ""])
        if issues:
            lines.extend(
                [
                    "| Severity | Category | Line | Finding | Recommended action |",
                    "|---|---|---:|---|---|",
                ]
            )
            for issue in issues[:50]:
                lines.append(
                    f"| {markdown_cell(issue.get('severity'))} | "
                    f"{markdown_cell(issue.get('category'))} | "
                    f"{markdown_cell(issue.get('line'))} | "
                    f"{markdown_cell(issue.get('message'))} | "
                    f"{markdown_cell(issue.get('suggestion'))} |"
                )
            lines.append("")
        else:
            lines.extend(["No issues were identified for this file.", ""])

    lines.extend(
        [
            "---",
            f"_Model: `{MODEL}` · Merge threshold: `{FAIL_ON_SEVERITY}` · Commit: `{os.getenv('GITHUB_HEAD_SHA', 'unknown')[:12]}`._",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary_file:
            summary_file.write("\n".join(lines))


def main() -> None:
    changed = get_changed_md_files()
    file_results: List[Dict[str, Any]] = []
    all_issues: List[Dict[str, Any]] = []

    if not changed:
        write_report(changed, file_results, all_issues)
        print("No docs/*.md changes detected. Skipping AI review.")
        return

    client = OpenAI()

    try:
        for file_name in changed:
            markdown_path = REPO_ROOT / file_name
            if not markdown_path.exists():
                continue

            prompt = {
                "file": file_name,
                "diff": get_diff_for_file(file_name),
                "content": markdown_path.read_text(encoding="utf-8"),
                "output_schema": {
                    "file": "string",
                    "summary": "string",
                    "issues": [
                        {
                            "severity": "minor|major|critical",
                            "category": "grammar|style|clarity|consistency|terminology|structure|risk",
                            "message": "string",
                            "suggestion": "string",
                            "line": "integer|null",
                        }
                    ],
                    "pass": "boolean",
                },
            }

            response = client.responses.create(
                model=MODEL,
                input=[
                    {"role": "system", "content": SYSTEM_RULES},
                    {
                        "role": "user",
                        "content": "Review this Markdown change set and return JSON using the output_schema. JSON only.",
                    },
                    {"role": "user", "content": json.dumps(prompt)},
                ],
                store=False,
            )

            text = response.output_text.strip()
            try:
                result = json.loads(text)
            except Exception as error:
                raise RuntimeError(
                    f"{file_name}: AI review did not return valid JSON: {error}. "
                    f"Response excerpt: {text[:1000]}"
                ) from error

            result["file"] = result.get("file") or file_name
            issues = result.get("issues", [])
            for issue in issues:
                issue["file"] = issue.get("file") or file_name
                annotate(issue)

            file_results.append(result)
            all_issues.extend(issues)

    except Exception as error:
        write_report(changed, file_results, all_issues, str(error))
        print(f"::error::{error}")
        raise

    write_report(changed, file_results, all_issues)

    worst = "minor"
    for issue in all_issues:
        severity = issue.get("severity", "minor")
        if SEVERITY_ORDER.get(severity, 0) > SEVERITY_ORDER.get(worst, 0):
            worst = severity

    if all_issues and severity_at_least(worst, FAIL_ON_SEVERITY):
        print(
            f"::error::AI review found {worst} issues "
            f"(threshold={FAIL_ON_SEVERITY})."
        )
        if not REPORT_ONLY:
            raise SystemExit(1)

    print("AI review completed.")


if __name__ == "__main__":
    main()
