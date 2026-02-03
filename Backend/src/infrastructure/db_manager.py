from sqlalchemy import create_engine, text

class DBManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)


    def fetch_all(self, query, params=None) -> list[dict]:
        """
        Execute a SELECT query and return all rows.
        Returns:
            list[dict]
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.mappings().all()

    def fetch_one(self, query, params=None) -> dict:
        """
        Execute a SELECT query and return the first row.
        Returns:
            dict | None
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.mappings().first()

    def execute(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        Raises an exception if the operation fails.
        """
        with self.engine.begin() as conn:
            conn.execute(text(query), params)
