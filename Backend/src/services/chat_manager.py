from sqlalchemy.exc import OperationalError
from src.repositories.chat_repo import ChatRepo
from src.infrastructure.llm import generate_answer
from src.services.errors import InvalidInput, DatabaseUnavailable, LLMUnavailable

SUMMARY_THRESHOLD = 6

class ChatManager:
    def __init__(self):
        self.repo = ChatRepo()

    def handle_message(self, user_id: int, text: str) -> dict:
        if not text:
            raise InvalidInput("Message cannot be empty")

        try:
            summary: dict = self.repo.get_summary(user_id)
            history: list[dict] = self.repo.get_last_messages(user_id, 5)
        except OperationalError:
            raise DatabaseUnavailable()

        context = []
        if summary and summary["summary"]:
            context.append(f"Summary: {summary['summary']}")

        for row in reversed(history):
            context.append(f"{row['role'].capitalize()}: {row['content']}")

        try:
            self.repo.add_message(user_id, "user", text)
        except OperationalError:
            raise DatabaseUnavailable()

        try:
            answer = generate_answer(text, history)
        except Exception as e:
            raise LLMUnavailable() from e

        try:
            self.repo.add_message(user_id, "assistant", answer)
            self.update_summary(user_id, summary)
        except OperationalError:
            raise DatabaseUnavailable()

        return {"status": "ok", "answer": answer}

    def update_summary(self, user_id, summary):
        if not summary:
            self.summarize_and_save(user_id)
            return

        new_count = self.repo.count_messages_after(user_id, summary["updated_at"])
        if new_count >= SUMMARY_THRESHOLD:
            self.summarize_and_save(user_id, new_count)

    def summarize_and_save(self, user_id, limit):
        old_summary_row = self.repo.get_summary(user_id)
        old_summary_text = old_summary_row["summary"] if old_summary_row else "No previous summary."

        messages = self.repo.get_last_messages(user_id, limit)
        
        new_chat_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in reversed(messages)]
        )

        prompt = f"""
        You are an assistant updating a conversation summary.
        
        EXISTING SUMMARY:
        {old_summary_text}
        
        NEW MESSAGES:
        {new_chat_text}
        
        INSTRUCTION:
        Create a new, concise summary that integrates the new messages into the existing summary. 
        Keep it brief but ensure no key nutritional information is lost.
        """

        try:
            new_summary = generate_answer(prompt, [])
            self.repo.save_summary(user_id, new_summary)
        except Exception:
            pass 