import os
import redis
import fakeredis
import json
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class CacheManager:
    """
    Gestor de cache configurable para usar Redis o fakeredis según el entorno.
    """

    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        cache_backend = os.getenv("CACHE_BACKEND", "redis").lower()

        if cache_backend == "redis":
            self.redis = self._connect()
            print("Using Redis as cache backend.")
        elif cache_backend == "fakeredis":
            self.redis = fakeredis.FakeStrictRedis()
            print("Using fakeredis as cache backend.")
        else:
            raise ValueError(f"Invalid CACHE_BACKEND: {cache_backend}")

    def _connect(self):
        """
        Conecta al servidor Redis.
        """
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        try:
            client = redis.Redis.from_url(redis_url)
            client.ping()
            return client
        except redis.ConnectionError as e:
            print(f"[ERROR] Could not connect to Redis: {str(e)}")
            raise Exception("Failed to connect to Redis. Check your configuration.")

    def save(self, key: str, data: dict):
        self.redis.setex(key, self.ttl, json.dumps(data))

    def get(self, key: str) -> dict:
        cached_data = self.redis.get(key)
        if cached_data:
            return json.loads(cached_data)
        return {}

    def delete(self, key: str):
        self.redis.delete(key)
