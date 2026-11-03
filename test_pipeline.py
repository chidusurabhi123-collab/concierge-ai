from app.ingestion.pipeline import ingest_file

files = [
    "data/documents/refund_policy.txt",
    "data/documents/sample.pdf"
]

for file in files:
    print(f"\n{'=' * 50}")
    print(f"FILE: {file}")

    chunks = ingest_file(file)

    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks:
        print("\n", chunk)