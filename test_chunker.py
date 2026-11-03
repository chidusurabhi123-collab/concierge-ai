from app.ingestion.chunker import sentence_chunker

text = """
Customers can request a refund within 7 days of receiving their order.
Refund requests must be reviewed by the support team.
Orders that have already been refunded cannot be refunded again.
"""

chunks = sentence_chunker(text, max_sentences=2)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i + 1}:")
    print(chunk)