import re


def sentence_chunker(text: str, max_sentences: int = 2) -> list[str]:
    if max_sentences <= 0:
        raise ValueError("max_sentences must be positive")

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []

    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i + max_sentences])
        chunks.append(chunk)

    return chunks
