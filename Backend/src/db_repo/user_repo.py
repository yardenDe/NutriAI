from app.dependencies import get_db_manager

class UserRepo:
    def __init__(self):
        self.db = get_db_manager

    def _dict_result(self, result):
        return [row._asdict() for row in result]

    def add_user(self, username: str, password: str):
        query = "SELECT add_user(:u, :p);"
        result = self.db.execute_query(query, {"u": username, "p": password})
        if result:
            return self._dict_result(result)[0]['add_user']
        return None

    def authenticate_user(self, username: str, password: str):
        query = "SELECT authenticate(:u, :p);"
        result = self.db.execute_query(query, {"u": username, "p": password})
        if result:
            return self._dict_result(result)[0]['authenticate']
        return None