from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv


class DBManager:
    def __init__(self):
        load_dotenv()
        self.engine = create_engine(
            os.getenv("DATABASE_URL", "sqlite:///local.db"),
        )

    def fetch_all(self, query, params=None):
        """
        Execute a SELECT query and return all rows.
        Returns:
            list[dict]
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.mappings().all()

    def fetch_one(self, query, params=None):
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
