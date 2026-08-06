from __future__ import annotations

import html
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
OUT_FILE = DOCS_DIR / "downloads.md"

EXCLUDED_NAMES = {"downloads.md"}
EXCLUDED_PARTS = {"includes"}


def include_page(path: pathlib.Path) -> bool:
    rel = path.relative_to(DOCS_DIR)
    return path.name not in EXCLUDED_NAMES and not any(part in EXCLUDED_PARTS for part in rel.parts)


def page_title(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")

    front_matter = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if front_matter:
        title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front_matter.group(1), re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

    heading = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if heading:
        return re.sub(r"\s+#+$", "", heading.group(1)).strip()

    return path.stem.replace("-", " ").replace("_", " ").title()


def source_link_for(rel: pathlib.Path) -> str:
    # downloads.md is located at the docs root, so source links remain docs-relative.
    return rel.as_posix()


def artifact_path(kind: str, rel: pathlib.Path, suffix: str) -> str:
    return f"{kind}/{rel.with_suffix(suffix).as_posix()}"


def main() -> None:
    pages = [path for path in sorted(DOCS_DIR.rglob("*.md")) if include_page(path)]

    lines = [
        "---",
        "title: Documentation downloads",
        "description: Download every published documentation page as HTML, PDF, or DOCX.",
        "tags:",
        "  - Publishing",
        "  - Downloads",
        "---",
        "",
        "# Documentation downloads",
        "",
        '<p class="downloads-intro">Every published page is generated in three reusable formats. '
        "Use HTML for browser-based sharing, PDF for controlled distribution and printing, "
        "and DOCX for downstream editing.</p>",
        "",
        '<div class="download-grid" aria-label="Available output formats">',
        '<div class="download-format"><strong>HTML</strong><span>Rendered page with the published site styling.</span></div>',
        '<div class="download-format"><strong>PDF</strong><span>A4 document with controlled margins and clean page breaks.</span></div>',
        '<div class="download-format"><strong>DOCX</strong><span>Editable Microsoft Word output generated from the rendered page.</span></div>',
        "</div>",
        "",
        '<div class="download-table" markdown>',
        "",
        "| Documentation page | Open online | HTML | PDF | DOCX |",
        "|---|---:|---:|---:|---:|",
    ]

    for page in pages:
        rel = page.relative_to(DOCS_DIR)
        title = html.escape(page_title(page))
        online = source_link_for(rel)
        html_file = artifact_path("html", rel, ".html")
        pdf_file = artifact_path("pdf", rel, ".pdf")
        docx_file = artifact_path("docx", rel, ".docx")
        lines.append(
            f'| {title} | [Open]({online}) | '
            f'<a href="{html_file}" download>HTML</a> | '
            f'<a href="{pdf_file}" download>PDF</a> | '
            f'<a href="{docx_file}" download>DOCX</a> |'
        )

    lines.extend(
        [
            "",
            "</div>",
            "",
            '!!! note "Build-generated files"',
            "    The links are populated by the GitHub Actions publishing workflow. "
            "A failed or incomplete export is blocked before the site is deployed.",
            "",
        ]
    )

    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUT_FILE} with {len(pages)} documentation pages.")


if __name__ == "__main__":
    main()
