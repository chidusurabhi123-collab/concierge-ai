from app.ingestion.pipeline import ingest_file
from app.retrieval.vector_store import VectorStore

files = [
    "data/documents/refund_policy.txt",
    "data/documents/sample.pdf"
]

all_chunks = []

for file in files:
    all_chunks.extend(ingest_file(file))

store = VectorStore()
store.build(all_chunks)
store.save()
print("Vector index saved successfully")

questions = [
    "How many days do customers have to request a refund?",
    "How long does standard delivery take?",
    "Can an already refunded order be refunded again?"
]

for question in questions:
    print(f"\nQUESTION: {question}")

    results = store.search(question, top_k=2)

    for result in results:
        print(f"\nScore: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Text: {result['text']}")