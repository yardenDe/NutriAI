from src.dependencies import get_db_manager

class SuppRepo:
    def __init__(self):
        self.db_manager = get_db_manager()

    def get_by_similarity(self, embedded_goal: str, top_n: int):
        query = """
        SELECT * 
        FROM find_supplements(cast(:goal as vector), :limit)
        """
        params = {"goal": embedded_goal, "limit": top_n}
        results = self.db_manager.fetch_all(query, params)
        return results

    def get_all(self):
        query = """
        SELECT name, description 
        FROM supplements;
        """
        results = self.db_manager.fetch_all(query)
        return results

    def get_by_name(self, name: str):
        query = """
        SELECT name, description 
        FROM supplements 
        WHERE name = :name
        """
        params = {"name": name}
        results = self.db_manager.fetch_one(query, params)
        return results