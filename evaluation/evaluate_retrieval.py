
import json
from pathlib import Path

from app.retrieval.vector_store import VectorStore

store = VectorStore()
store.load()

with open("evaluation/questions.json", encoding="utf-8") as file:
    questions = json.load(file)

TP = FP = TN = FN = 0

for item in questions:
    results = store.search(item["question"], top_k=3)

    retrieved = any(
        result["score"] >= 0.45
        for result in results
    )

    expected = item["expected_behavior"] == "answer"

    if expected and retrieved:
        TP += 1
        outcome = "TP"
    elif not expected and retrieved:
        FP += 1
        outcome = "FP"
    elif not expected and not retrieved:
        TN += 1
        outcome = "TN"
    else:
        FN += 1
        outcome = "FN"

    print(f"{outcome} | Q{item['id']} | {item['question']}")

total = len(questions)

print("\n========== RETRIEVAL EVALUATION ==========")
print(f"Total: {total}")
print(f"True Positives: {TP}")
print(f"False Positives: {FP}")
print(f"True Negatives: {TN}")
print(f"False Negatives: {FN}")
print(f"Accuracy: {(TP + TN) / total * 100:.2f}%")

precision = TP / (TP + FP) if TP + FP else 0
recall = TP / (TP + FN) if TP + FN else 0

print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
