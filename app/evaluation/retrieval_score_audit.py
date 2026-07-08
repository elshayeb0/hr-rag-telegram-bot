from app.retrieval.retriever import retrieve_chunks

questions = [
    "What should an employee do on the first day of sickness?",
    "What is the sick leave policy?",
    "What is the maternity policy?",
    "What is the BYOD policy?",
    "What is the alcohol policy?",
    "What is the company's remote work policy?",
    "What is my salary?",
    "How old am I?",
    "What is the CEO policy?",
]

for question in questions:
    chunks = retrieve_chunks(question, user_groups=["employee"])
    print(f"\nQUESTION: {question}")

    if not chunks:
        print("  No chunks retrieved")
        continue

    for chunk in chunks:
        print(f"  score={chunk.score:.4f} | source={chunk.source} | chunk_id={chunk.chunk_id}")
