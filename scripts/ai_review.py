import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List
from openai import OpenAI

REPORT_ONLY = os.getenv("AI_REVIEW_REPORT_ONLY", "0").lower() in ("1", "true", "yes")

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

# Tune these:
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # cheaper/faster; change to gpt-5 if you want
FAIL_ON_SEVERITY = os.getenv("FAIL_ON_SEVERITY", "critical").lower()  # minor|major|critical

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
    # On PRs, GitHub provides base/head SHAs
    base = os.getenv("GITHUB_BASE_SHA")
    head = os.getenv("GITHUB_HEAD_SHA")
    if not base or not head:
        # fallback: compare against origin/main (best-effort)
        base = "origin/main"
        head = "HEAD"

    out = run(["git", "diff", "--name-only", f"{base}...{head}"])
    files = [f for f in out.splitlines() if f.startswith("docs/") and f.endswith(".md")]
    # Avoid reviewing auto-generated downloads page if you have it
    files = [f for f in files if not f.endswith("docs/downloads.md")]
    return files

def get_diff_for_file(path: str) -> str:
    base = os.getenv("GITHUB_BASE_SHA") or "origin/main"
    head = os.getenv("GITHUB_HEAD_SHA") or "HEAD"
    return run(["git", "diff", f"{base}...{head}", "--", path])

def severity_at_least(sev: str, threshold: str) -> bool:
    return SEVERITY_ORDER.get(sev, 0) >= SEVERITY_ORDER.get(threshold, 2)

def annotate(issue: Dict[str, Any]) -> None:
    # GitHub annotation format: ::warning file=...,line=...::message
    sev = issue.get("severity", "minor")
    level = "warning"
    if sev == "critical":
        level = "error"
    elif sev == "major":
        level = "warning"

    file = issue.get("file", "")
    line = issue.get("line")
    msg = issue.get("message", "Issue")
    suggestion = issue.get("suggestion", "")

    full = msg if not suggestion else f"{msg} | Suggestion: {suggestion}"

    if file and line:
        print(f"::{level} file={file},line={line}::{full}")
    elif file:
        print(f"::{level} file={file}::{full}")
    else:
        print(f"::{level}::{full}")

def main():
    changed = get_changed_md_files()
    if not changed:
        print("No docs/*.md changes detected. Skipping AI review.")
        return

    client = OpenAI()  # uses OPENAI_API_KEY from env
    all_issues: List[Dict[str, Any]] = []

    for f in changed:
        md_path = REPO_ROOT / f
        if not md_path.exists():
            continue

        content = md_path.read_text(encoding="utf-8")
        diff = get_diff_for_file(f)

        prompt = {
            "file": f,
            "diff": diff,
            "content": content,
            "output_schema": {
                "file": "string",
                "summary": "string",
                "issues": [
                    {
                        "severity": "minor|major|critical",
                        "category": "grammar|style|clarity|consistency|terminology|structure|risk",
                        "message": "string",
                        "suggestion": "string",
                        "line": "integer|null"
                    }
                ],
                "pass": "boolean"
            }
        }

        resp = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_RULES},
                {"role": "user", "content": "Review this Markdown change set and return JSON using the output_schema. JSON only."},
                {"role": "user", "content": json.dumps(prompt)}
            ],
            # store false avoids server-side storage if you prefer
            store=False,
        )

        # Responses API helper
        text = resp.output_text.strip()
        try:
            result = json.loads(text)
        except Exception as e:
            print(f"::error::{f}: AI review did not return valid JSON. Error: {e}")
            print(text[:1500])
            raise

        issues = result.get("issues", [])
        for i in issues:
            i["file"] = i.get("file", f) or f
            annotate(i)
        all_issues.extend(issues)

        # Write to step summary (Actions UI)
        summary_path = os.getenv("GITHUB_STEP_SUMMARY")
        if summary_path:
            with open(summary_path, "a", encoding="utf-8") as s:
                s.write(f"## AI Review: `{f}`\n\n")
                s.write(result.get("summary", "") + "\n\n")
                if issues:
                    s.write("| Severity | Category | Message |\n|---|---|---|\n")
                    for i in issues[:50]:
                        s.write(f"| {i.get('severity')} | {i.get('category')} | {i.get('message')} |\n")
                    s.write("\n")

    # Decide pass/fail
    worst = "minor"
    for i in all_issues:
        sev = i.get("severity", "minor")
        if SEVERITY_ORDER.get(sev, 0) > SEVERITY_ORDER.get(worst, 0):
            worst = sev

    if severity_at_least(worst, FAIL_ON_SEVERITY):
         print(f"::error::AI review found {worst} issues (threshold={FAIL_ON_SEVERITY}).")
         if not REPORT_ONLY:
             raise SystemExit(1)


    print("AI review passed.")

if __name__ == "__main__":
    main()
