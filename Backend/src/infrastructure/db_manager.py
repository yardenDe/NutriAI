from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

class DB_Manager:
    """Handles any database interactions using SQLAlchemy."""
    def __init__(self):
        load_dotenv()
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
        self.engine = create_engine(self.db_url)
       
    def execute_query(self, query, params=None):
        """Handles read-only queries"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                return result
        except Exception as e:
            raise e

    def execute_transaction(self, query, params=None):
        """Handles all queries"""
        try:
            with self.engine.begin() as conn:
                return conn.execute(text(query), params)
        except Exception as e:
            raise e
        
