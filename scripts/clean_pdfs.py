from __future__ import annotations

import pathlib
import shutil
import tempfile

from pypdf import PdfReader, PdfWriter

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"
OUT_DIR = SITE_DIR / "downloads" / "pdf"

EXCLUDED_NAMES = {"downloads.md"}
EXCLUDED_PARTS = {"includes"}


def include_page(path: pathlib.Path) -> bool:
    rel = path.relative_to(DOCS_DIR)
    return path.name not in EXCLUDED_NAMES and not any(part in EXCLUDED_PARTS for part in rel.parts)


def generated_pdf_path(rel: pathlib.Path) -> pathlib.Path:
    if rel.name == "index.md":
        candidates = [
            SITE_DIR / rel.parent / "index.pdf",
            SITE_DIR / rel.parent / "index" / "index.pdf",
        ]
    else:
        route = rel.with_suffix("")
        candidates = [
            SITE_DIR / route / f"{rel.stem}.pdf",
            SITE_DIR / rel.with_suffix(".pdf"),
            SITE_DIR / route / "index.pdf",
        ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(f"No generated PDF found for {rel}. Checked: {candidates}")


def has_visual_content(page) -> bool:
    text = (page.extract_text() or "").strip()
    if text:
        return True

    resources = page.get("/Resources")
    if resources is None:
        return False

    try:
        resources = resources.get_object()
    except AttributeError:
        pass

    xobjects = resources.get("/XObject") if hasattr(resources, "get") else None
    if xobjects:
        try:
            xobjects = xobjects.get_object()
        except AttributeError:
            pass
        if len(xobjects) > 0:
            return True

    return False


def remove_blank_pages(source: pathlib.Path) -> None:
    reader = PdfReader(str(source))
    keep = [page for page in reader.pages if has_visual_content(page)]

    if not keep or len(keep) == len(reader.pages):
        return

    writer = PdfWriter()
    for page in keep:
        writer.add_page(page)

    with tempfile.NamedTemporaryFile(
        prefix=f"{source.stem}-",
        suffix=".pdf",
        dir=source.parent,
        delete=False,
    ) as temporary:
        temp_path = pathlib.Path(temporary.name)

    try:
        with temp_path.open("wb") as stream:
            writer.write(stream)
        temp_path.replace(source)
    finally:
        temp_path.unlink(missing_ok=True)

    print(f"Removed {len(reader.pages) - len(keep)} blank page(s) from {source}.")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if not include_page(md_file):
            continue

        rel = md_file.relative_to(DOCS_DIR)
        source = generated_pdf_path(rel)
        remove_blank_pages(source)

        destination = OUT_DIR / rel.with_suffix(".pdf")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        count += 1

    print(f"Prepared {count} cleaned PDF downloads in {OUT_DIR}.")


if __name__ == "__main__":
    main()
