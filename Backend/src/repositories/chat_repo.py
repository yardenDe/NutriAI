from src.infrastructure.db_manager import DBManager

class ChatRepo:
    def __init__(self):
        self.db = DBManager()

    def get_summary(self, user_id: int):
        query = """
        SELECT summary
        FROM chat_summaries
        WHERE user_id = :user_id
        """
        params = {"user_id": user_id}
        return self.db.fetch_one(query, params)

    def save_summary(self, user_id: int, summary: str):
        query = """
        INSERT INTO chat_summary (user_id, summary, updated_at)
        VALUES (:user_id, :summary, NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET summary = EXCLUDED.summary, updated_at = NOW()
        """
        params = {"user_id": user_id, "summary": summary}
        self.db.execute(query, params)

    def get_last_messages(self, user_id: int, limit: int):
        query = """
        SELECT role, content
        FROM chat_messages
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT :limit
        """
        params = {"user_id": user_id, "limit": limit}
        return self.db.fetch_all(query, params)

    def add_message(self, user_id: int, role: str, content: str):
        query = """
        INSERT INTO chat_messages (user_id, role, content)
        VALUES (:user_id, :role, :content)
        """
        params = {
            "user_id": user_id,
            "role": role,
            "content": content
        }
        self.db.execute(query, params)

    def count_messages_after(self, user_id: int, since):
        query = """
        SELECT COUNT(*) as c
        FROM chat_history
        WHERE user_id = :user_id
        AND created_at > :since
        """
        params = {"user_id": user_id, "since": since}
        row = self.db.fetch_one(query, params)
        return row["c"]
