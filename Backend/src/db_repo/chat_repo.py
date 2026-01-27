from app.dependencies import get_db_manager

class ChatRepo:
    def __init__(self):
        self.db = get_db_manager

    def _dict_result(self, result):
        return [row._asdict() for row in result]

    def add_chat_message(self, user_id: int, role: str, content: str):
        query = "SELECT add_chat_message(:uid, :role, :content);"
        params = {"uid": user_id, "role": role, "content": content}
        self.db.execute_transaction(query, params)

    def get_last_messages(self, user_id: int, limit: int = 5):
        query = "SELECT * FROM get_last_messages(:uid, :limit);"
        results = self.db.execute_query(query, {"uid": user_id, "limit": limit})
        return self._dict_result(results)

    def get_chat_summary(self, user_id: int):
        query = "SELECT get_chat_summary(:uid);"
        result = self.db.execute_query(query, {"uid": user_id})
        if result:
            return self._dict_result(result)[0]['get_chat_summary']
        return None

    def update_chat_summary(self, user_id: int, summary: str):
        query = "SELECT update_chat_summary(:uid, :summary);"
        self.db.execute_transaction(query, {"uid": user_id, "summary": summary})

    def get_last_summary_time(self, user_id: int):
        query = "SELECT get_summary_time(:uid);"
        result = self.db.execute_query(query, {"uid": user_id})
        if result:
            return self._dict_result(result)[0]['get_summary_time']
        return None

    def count_new_messages(self, user_id: int, last_summary_time):
        query = "SELECT count_new_messages(:uid, :lst);"
        params = {"uid": user_id, "lst": last_summary_time}
        result = self.db.execute_query(query, params)
        if result:
            return self._dict_result(result)[0]['count_new_messages']
        return 0