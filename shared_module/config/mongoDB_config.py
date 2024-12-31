from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

class MongoDBConfig:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

# Inicializar la configuración de MongoDB
mongodb_config = MongoDBConfig(
    uri="mongodb://localhost:27017/",
    db_name="bugster_db"
)
