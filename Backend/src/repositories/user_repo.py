from src.dependencies import get_db_manager


class UserRepo:
    def __init__(self):
        self.db = get_db_manager()

    def add_user(self, username: str, password: str):
        query = """
        INSERT INTO users (username, password)
        VALUES (:username, :password)
        """
        params = {
            "username": username,
            "password": password
        }
        self.db.execute(query, params)

    def get_user(self, username: str):
        query = """
        SELECT id, password
        FROM users
        WHERE username = :username
        """
        params = {
            "username": username
        }
        return self.db.fetch_one(query, params)
