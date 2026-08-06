from __future__ import annotations

import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"

EXCLUDED_NAMES = {"downloads.md"}
EXCLUDED_PARTS = {"includes"}


def include_page(path: pathlib.Path) -> bool:
    rel = path.relative_to(DOCS_DIR)
    return path.name not in EXCLUDED_NAMES and not any(part in EXCLUDED_PARTS for part in rel.parts)


def main() -> None:
    failures: list[str] = []
    pages = [path for path in sorted(DOCS_DIR.rglob("*.md")) if include_page(path)]

    downloads_page = SITE_DIR / "downloads" / "index.html"
    if not downloads_page.is_file():
        failures.append(f"Missing downloads page: {downloads_page}")

    for md_file in pages:
        rel = md_file.relative_to(DOCS_DIR)
        for kind, suffix in (("pdf", ".pdf"), ("docx", ".docx")):
            artifact = SITE_DIR / "downloads" / kind / rel.with_suffix(suffix)
            if not artifact.is_file():
                failures.append(f"Missing {kind.upper()} artifact: {artifact}")
            elif artifact.stat().st_size == 0:
                failures.append(f"Empty {kind.upper()} artifact: {artifact}")

    if failures:
        print("Download verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Verified the downloads page and {len(pages) * 2} generated files.")


if __name__ == "__main__":
    main()
