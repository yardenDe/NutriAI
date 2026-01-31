from src.dependencies import get_llm

def _build_prompt(input: str, context: list[str]) -> str:
    context_text = "\n".join(context) if context else "No prior context."

    return f"""
You are a helpful assistant.

Conversation context:
{context_text}

User message:
{input}

Assistant:
""".strip()


def generate_answer(input: str, context: list[str]) -> str:
    model, client = get_llm()

    prompt = _build_prompt(input, context)

    chat = client.chats.create(model=model)
    response = chat.send_message(prompt)

    return response.text.strip()
