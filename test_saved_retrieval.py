from app.retrieval.vector_store import VectorStore

store = VectorStore()

# Load previously saved index
store.load()

print("Saved index loaded successfully")

questions = [
    "What is the refund period?",
    "What is the standard delivery time?",
    "Can customers get a refund twice?"
]

for question in questions:
    print(f"\nQUESTION: {question}")

    results = store.search(question, top_k=2)

    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Page: {result['page']}")
        print(f"Text: {result['text']}")