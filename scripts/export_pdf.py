from __future__ import annotations

import pathlib
import shutil
import subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"
OUT_DIR = SITE_DIR / "downloads" / "pdf"

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


def chrome_binary() -> str:
    for command in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(command)
        if path:
            return path
    raise FileNotFoundError("No supported Chromium or Google Chrome executable was found.")


def export_pdf(browser: str, source: pathlib.Path, destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_url = source.resolve().as_uri()

    subprocess.run(
        [
            browser,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--allow-file-access-from-files",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=2500",
            f"--print-to-pdf={destination.resolve()}",
            source_url,
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if not destination.is_file() or destination.stat().st_size == 0:
        raise RuntimeError(f"Chrome did not create a valid PDF: {destination}")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    browser = chrome_binary()
    count = 0

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if not include_page(md_file):
            continue

        rel = md_file.relative_to(DOCS_DIR)
        source = rendered_html_path(rel)
        destination = OUT_DIR / rel.with_suffix(".pdf")
        export_pdf(browser, source, destination)
        count += 1

    print(f"Exported {count} per-page PDF files with {pathlib.Path(browser).name}.")


if __name__ == "__main__":
    main()
