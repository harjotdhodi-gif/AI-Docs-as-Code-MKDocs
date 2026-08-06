from __future__ import annotations

import pathlib
import shutil
import subprocess
import tempfile

from bs4 import BeautifulSoup

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"
OUT_DIR = SITE_DIR / "downloads" / "docx"

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


def article_html(source: pathlib.Path) -> str:
    soup = BeautifulSoup(source.read_text(encoding="utf-8"), "html.parser")
    article = soup.select_one("article.md-content__inner") or soup.select_one("main") or soup.body
    if article is None:
        raise ValueError(f"No document content found in {source}")

    for selector in (
        ".md-content__button",
        ".md-source-file",
        "script",
        "style",
        "noscript",
    ):
        for node in article.select(selector):
            node.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else source.stem
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title></head><body>{article}</body></html>"
    )


def run_pandoc(source_html: pathlib.Path, destination: pathlib.Path, resource_path: pathlib.Path) -> None:
    subprocess.run(
        [
            "pandoc",
            str(source_html),
            "--from=html",
            "--to=docx",
            "--standalone",
            f"--resource-path={resource_path}:{SITE_DIR}",
            "--output",
            str(destination),
        ],
        check=True,
    )


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    with tempfile.TemporaryDirectory(prefix="mkdocs-docx-") as temp_dir:
        temp_root = pathlib.Path(temp_dir)

        for md_file in sorted(DOCS_DIR.rglob("*.md")):
            if not include_page(md_file):
                continue

            rel = md_file.relative_to(DOCS_DIR)
            rendered = rendered_html_path(rel)
            temp_html = temp_root / rel.with_suffix(".html")
            temp_html.parent.mkdir(parents=True, exist_ok=True)
            temp_html.write_text(article_html(rendered), encoding="utf-8")

            destination = OUT_DIR / rel.with_suffix(".docx")
            destination.parent.mkdir(parents=True, exist_ok=True)
            run_pandoc(temp_html, destination, rendered.parent)
            count += 1

    print(f"Exported {count} DOCX files to {OUT_DIR}.")


if __name__ == "__main__":
    main()
