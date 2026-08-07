from __future__ import annotations

import pathlib
import shutil

from bs4 import BeautifulSoup

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"
OUT_DIR = SITE_DIR / "downloads" / "html"
SITE_URL = "https://harjotdhodi-gif.github.io/AI-Docs-as-Code-MKDocs/"

EXCLUDED_NAMES = {"downloads.md"}
EXCLUDED_PARTS = {"includes"}


def include_page(path: pathlib.Path) -> bool:
    rel = path.relative_to(DOCS_DIR)
    return path.name not in EXCLUDED_NAMES and not any(part in EXCLUDED_PARTS for part in rel.parts)


def rendered_html_path(rel: pathlib.Path) -> pathlib.Path:
    if rel.name == "index.md":
        candidates = [SITE_DIR / rel.parent / "index.html"]
    else:
        candidates = [
            SITE_DIR / rel.with_suffix("") / "index.html",
            SITE_DIR / rel.with_suffix(".html"),
        ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(f"No rendered HTML found for {rel}. Checked: {candidates}")


def make_downloadable_copy(source: pathlib.Path, destination: pathlib.Path) -> None:
    soup = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")

    if soup.head is not None:
        existing_base = soup.head.find("base")
        if existing_base is not None:
            existing_base.decompose()
        base = soup.new_tag("base", href=SITE_URL)
        soup.head.insert(0, base)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(str(soup), encoding="utf-8")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if not include_page(md_file):
            continue

        rel = md_file.relative_to(DOCS_DIR)
        source = rendered_html_path(rel)
        destination = OUT_DIR / rel.with_suffix(".html")
        make_downloadable_copy(source, destination)
        count += 1

    print(f"Exported {count} downloadable HTML files to {OUT_DIR}.")


if __name__ == "__main__":
    main()
