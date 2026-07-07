ANSWER_PROMPT = """
Answer the user's question using the retrieved company document context.

User question:
{question}

Retrieved context:
{context}

Return:
1. Direct answer
2. Brief explanation
3. Sources section

If the context does not answer the question, say:
"I do not have enough information from the official company documents to answer this confidently."
"""
