from pathlib import Path

from app.ingestion.loader import load_txt, load_pdf
from app.ingestion.chunker import sentence_chunker


def ingest_file(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".txt":
        document = load_txt(path)

        pages = [{
            "page": None,
            "content": document["content"]
        }]

    elif path.suffix.lower() == ".pdf":
        document = load_pdf(path)
        pages = document["pages"]

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    all_chunks = []

    for page in pages:
        chunks = sentence_chunker(
            page["content"],
            max_sentences=2
        )

        for chunk in chunks:
            all_chunks.append({
                "chunk_id": len(all_chunks),
                "text": chunk,
                "source": document["filename"],
                "page": page["page"]
            })

    return all_chunks