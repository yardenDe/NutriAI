from src.infrastructure.db_manager import DBManager
from src.infrastructure.token_provider import TokenProvider

db_connection = None
token_provider = None

def get_db_manager():
    global db_connection
    if db_connection is None:
        db_connection = DBManager() 

    return db_connection

def get_token_provider():
    global token_provider
    if token_provider is None:
        token_provider = TokenProvider() 

    return token_provider