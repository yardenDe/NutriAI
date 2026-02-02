
def extract_symptoms_prompt(text: str) -> str:
    return f"""
    Extract health-related symptoms from the text below.

    Rules:
    - Return a JSON array of symptom names only.
    - If no health-related symptoms are mentioned, return an empty JSON array: [].
    - Do not add explanations or extra text.

    Text:
    {text}
    """.strip()


def answer_with_context_prompt(
    question: str,
    rag_context: str,
    chat_context: str,
) -> str:
    return f"""
    You are a professional nutrition expert.

    Conversation context:
    {chat_context}

    Relevant nutritional context:
    {rag_context}

    User question:
    {question}

    Instructions:
    - Use the provided context to answer the user's question.
    - Be clear, practical, and evidence-based.
    - If the context is insufficient, say so honestly.
    - Do NOT return JSON.
    - Answer in natural language suitable for a user.

    Answer:
    """.strip()

def summarize_chat_history_prompt(old_summary: str, new_messages: str) -> str:
    return f"""
    You are an assistant updating a conversation summary.

    EXISTING SUMMARY:
    {old_summary}

    NEW MESSAGES:
    {new_messages}

    INSTRUCTION:
    Create a concise updated summary that preserves important information from both the existing summary and the new messages. 
    Keep it to 3-4 sentences maximum.
    """.strip()
