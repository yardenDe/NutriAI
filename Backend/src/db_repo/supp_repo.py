class SuppRepo:
    def __init__(self, db_manager):
        self.db = db_manager

    def _dict_result(self, result):
        return [row._asdict() for row in result]

    def find_similar(self, embedded_goal: str, top_n: int):
        query = "SELECT * FROM find_supplements(:goal, :limit);"
        params = {"goal": embedded_goal, "limit": top_n}
        results = self.db.execute_query(query, params)
        return self._dict_result(results)

    def get_all(self):
        query = "SELECT name, description FROM supplements;"
        results = self.db.execute_query(query)
        return self._dict_result(results)

    def get_by_name(self, name: str):
        query = "SELECT name, description FROM supplements WHERE name = :name;"
        results = self.db.execute_query(query, {"name": name})
        return self._dict_result(results)