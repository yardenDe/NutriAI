import logging
from typing import List, Dict, Optional
from src.dependencies import get_db_manager

logger = logging.getLogger(__name__)

class ChatRepo:
    def __init__(self):
        self.db_manager = get_db_manager()

    def add_chat_message(self, user_id: int, role: str, content: str):
        query = "SELECT add_chat_message(:uid, :role, :content);"
        params = {"uid": user_id, "role": role, "content": content}
        self.db_manager.execute_transaction(query, params)

    def get_last_messages(self, user_id: int, limit: int = 5) -> List[Dict]:
        query = "SELECT * FROM get_last_messages(:uid, :limit);"
        return self.db_manager.execute_query(query, {"uid": user_id, "limit": limit})

    def get_chat_summary(self, user_id: int) -> Optional[str]:
        query = "SELECT get_chat_summary(:uid);"
        results = self.db_manager.execute_query(query, {"uid": user_id})
        
        if results:
            return results[0].get('get_chat_summary')
        return None

    def update_chat_summary(self, user_id: int, summary: str):
        query = "SELECT update_chat_summary(:uid, :summary);"
        self.db_manager.execute_transaction(query, {"uid": user_id, "summary": summary})

    def get_last_summary_time(self, user_id: int):
        query = "SELECT get_summary_time(:uid);"
        results = self.db_manager.execute_query(query, {"uid": user_id})
        
        if results:
            return results[0].get('get_summary_time')
        return None

    def count_new_messages(self, user_id: int, last_summary_time) -> int:
        query = "SELECT count_new_messages(:uid, :lst);"
        params = {"uid": user_id, "lst": last_summary_time}
        results = self.db_manager.execute_query(query, params)
        
        if results:
            return results[0].get('count_new_messages', 0)
        return 0