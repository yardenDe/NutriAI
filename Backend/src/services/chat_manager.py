import logging
from sqlalchemy.exc import OperationalError
from src.services.rag_pipline import rag_pipeline
from src.services.prompts import summarize_chat_history_prompt
from src.repositories.chat_repo import ChatRepo
from src.dependencies import get_llm
from src.services.errors import InvalidInput

# Initialize logger
logger = logging.getLogger(__name__)

MAX_MESSAGES = 5

class ChatManager:
    def __init__(self):
        self.repo = ChatRepo()
        self.llm_service = get_llm()

    def handle_message(self, user_id: int, user_input: str) -> dict:
        """
        Main entry point for handling chat messages with multi-level fallback logic.
        """
        if not user_input or not user_input.strip():
            raise InvalidInput("Message cannot be empty")

        summary, history, context = None, [], ""
        db_alive = True

        # Phase 1: Context Building & Persistence
        try:
            self.repo.add_message(user_id, "user", user_input)
            summary = self.repo.get_summary(user_id)
            history = self.repo.get_last_messages(user_id, 5)
            context = self._build_context(summary, history)
        except OperationalError:
            # If DB is down, mark it and proceed to fallback later
            logger.error("Database unavailable during context building")
            db_alive = False

        # Phase 2: RAG Pipeline execution (only if DB is accessible)
        answer = None
        if db_alive:
            try:
                answer = rag_pipeline(user_input, context)
            except Exception as e:
                logger.error(f"RAG pipeline failure: {e}")

        # Phase 3: Fallback logic if RAG failed, returned None, or DB is down
        if not answer:
            answer = self._handle_fallback(user_input, context, db_alive)

        # Phase 4: Final DB persistence (save assistant response if possible)
        if db_alive:
            try:
                self.repo.add_message(user_id, "assistant", answer)
                self._update_summary_if_needed(user_id, summary)
            except OperationalError:
                logger.warning("Could not save assistant response due to DB error")

        return {
            "status": "ok",
            "answer": answer
        }

    def _handle_fallback(self, user_input: str, context: str, db_alive: bool) -> str:
        """
        Generates a fallback response based on the specific failure point.
        Adds a relevant prefix to inform the user about the system status.
        """
        if not db_alive:
            # Case 1: Database is completely unreachable
            prefix = "[Note: Our database is currently offline. Answering without history or specific recommendations]\n\n"
            prompt = f"User: {user_input}\nAssistant:"
        
        elif not context:
            # Case 2: DB is alive but no chat history/context was found
            prefix = "[Note: Answering without previous conversation context]\n\n"
            prompt = f"User: {user_input}\nAssistant:"
            
        else:
            # Case 3: DB and Context are fine, but RAG found no relevant supplements
            prefix = "[Note: No specific supplements found in our database for this query. Providing a general response]\n\n"
            prompt = f"Context: {context}\nUser: {user_input}\nAssistant:"

        # Generate the actual text from LLM
        llm_response = self.llm_service.generate(prompt)
        return f"{prefix}{llm_response}"

    def _build_context(self, summary: dict, history: list) -> str:
        """
        Combines summary and recent history into a single string.
        """
        context_parts = []
        if summary and summary.get("summary"):
            context_parts.append(f"Summary: {summary['summary']}")
        
        for msg in reversed(history):
            context_parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
            
        return " ".join(context_parts)

    def _update_summary_if_needed(self, user_id: int, summary: dict):
        if not summary:
            self._summarize_and_save(user_id)
            return

        new_count = self.repo.count_messages_after(user_id, summary["updated_at"])
        if new_count >= MAX_MESSAGES:
            self._summarize_and_save(user_id)

    def _summarize_and_save(self, user_id: int):
        try:
            summary = self.repo.get_summary(user_id)
            old_summary = summary["summary"] if summary else "No previous summary."
            
            messages = self.repo.get_last_messages(user_id, MAX_MESSAGES)
            chat_text = "\n".join(f"{m['role']}: {m['content']}" for m in reversed(messages))
            
            prompt = summarize_chat_history_prompt(old_summary, chat_text)
            new_summary = self.llm_service.generate(prompt)
            self.repo.save_summary(user_id, new_summary)
        except Exception as e:
            logger.warning(f"Summary update failed for user {user_id}: {e}")