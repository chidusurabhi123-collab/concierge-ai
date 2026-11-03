
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )
        self.index = None
        self.chunks = []

    def build(self, chunks: list[dict]):
        if not chunks:
            raise ValueError("Cannot build index with zero chunks")

        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Build or load the index first")

        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks))
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            result = self.chunks[idx].copy()
            result["score"] = float(score)
            results.append(result)

        return results

    def save(self, directory: str = "storage"):
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)

        if self.index is None:
            raise RuntimeError("Build the index before saving")

        faiss.write_index(self.index, str(path / "index.faiss"))

        with open(path / "chunks.json", "w", encoding="utf-8") as file:
            json.dump(self.chunks, file, ensure_ascii=False, indent=2)

    def load(self, directory: str = "storage"):
        path = Path(directory)

        self.index = faiss.read_index(str(path / "index.faiss"))

        with open(path / "chunks.json", "r", encoding="utf-8") as file:
            self.chunks = json.load(file)

	