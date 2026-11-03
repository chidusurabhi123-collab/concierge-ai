
from pathlib import Path
from typing import Any

import pymupdf


def load_txt(file_path: str | Path) -> dict[str, str]:
    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    return {
        "filename": path.name,
        "content": text,
        "file_type": "txt"
    }


def load_pdf(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)

    pages = []

    with pymupdf.open(path) as document:
        for page_number in range(document.page_count):
            page = document.load_page(page_number)
            text = page.get_text()

            pages.append({
                "page": page_number + 1,
                "content": text
            })

    return {
        "filename": path.name,
        "pages": pages,
        "file_type": "pdf"
    }
