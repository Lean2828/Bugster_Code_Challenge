import os
from database_manager import DatabaseManager
from pymongo.collection import Collection
from config.mongoDB_config import mongodb_config


from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

db_uri = os.getenv("DB_URI")
db_name = os.getenv("DB_NAME")

def get_database_manager() -> DatabaseManager:
    """
    Retorna una instancia de DatabaseManager.
    """
    return DatabaseManager(uri=db_uri, db_name=db_name)

