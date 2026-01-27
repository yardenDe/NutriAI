from src.db_repo.chat_repo import ChatRepo
from src.infrastructure.llm import generate_answer


class ChatManager:
    """
    Handles the chat flow:
    - loads history & summary
    - calls the LLM
    - persists messages
    """

    def __init__(self):
        self.repo = ChatRepo()

    def handle_message(self, user_id: int, text: str) -> str:
        # Load summary & recent history
        summary = self.repo.get_chat_summary(user_id)
        history_rows = self.repo.get_last_messages(user_id, 5)

        history = []
        if summary:
            history.append(f"Summary: {summary}")

        for row in reversed(history_rows):
            history.append(f"{row['role'].capitalize()}: {row['content']}")

        # Save user message
        self.repo.add_chat_message(user_id, "user", text)

        # Ask LLM
        answer = generate_answer(
            user_text=text,
            context=history
        )

        # Save assistant answer
        self.repo.add_chat_message(user_id, "assistant", answer)

        # Update summary if needed
        self.repo.update_summary_if_needed(user_id)

        return answer
