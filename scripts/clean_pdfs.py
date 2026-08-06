from __future__ import annotations

import pathlib
import tempfile

from pypdf import PdfReader, PdfWriter

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF_DIR = REPO_ROOT / "site" / "downloads" / "pdf"


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
        return len(xobjects) > 0

    return False


def remove_blank_pages(pdf_path: pathlib.Path) -> int:
    reader = PdfReader(str(pdf_path))
    retained = [page for page in reader.pages if has_visual_content(page)]

    if not retained:
        raise RuntimeError(f"PDF contains no visible pages: {pdf_path}")

    removed = len(reader.pages) - len(retained)
    if removed == 0:
        return 0

    writer = PdfWriter()
    for page in retained:
        writer.add_page(page)

    with tempfile.NamedTemporaryFile(
        prefix=f"{pdf_path.stem}-",
        suffix=".pdf",
        dir=pdf_path.parent,
        delete=False,
    ) as temporary:
        temp_path = pathlib.Path(temporary.name)

    try:
        with temp_path.open("wb") as stream:
            writer.write(stream)
        temp_path.replace(pdf_path)
    finally:
        temp_path.unlink(missing_ok=True)

    return removed


def main() -> None:
    pdf_files = sorted(PDF_DIR.rglob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No generated PDFs found under {PDF_DIR}")

    total_removed = 0
    for pdf_file in pdf_files:
        removed = remove_blank_pages(pdf_file)
        total_removed += removed
        if removed:
            print(f"Removed {removed} blank page(s) from {pdf_file}.")

    print(f"Checked {len(pdf_files)} PDFs; removed {total_removed} blank page(s).")


if __name__ == "__main__":
    main()
