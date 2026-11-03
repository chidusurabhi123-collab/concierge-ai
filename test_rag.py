from app.services.rag import answer_question

questions = [
    "How many days do customers have to request a refund?",
    "How long does standard delivery take?",
    "Can an already refunded order be refunded again?",
    "What is the CEO's phone number?",
    "Can I get a refund after 90 days?",
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = answer_question(question)

    print("\nANSWER:", result["answer"])
    print("SOURCES:", result["sources"])
    print("ESCALATION:", result.get("escalation_required", False))