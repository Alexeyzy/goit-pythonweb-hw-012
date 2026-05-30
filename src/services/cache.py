import pickle

import redis

from src.conf.config import settings

redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)


def get_cache(key: str):
    """Return Python object from Redis."""
    value = redis_client.get(key)
    return pickle.loads(value) if value else None


def set_cache(key: str, value, expire: int = 900) -> None:
    """Save Python object to Redis."""
    redis_client.set(key, pickle.dumps(value), ex=expire)


def delete_cache(key: str) -> None:
    """Delete Redis cache key."""
    redis_client.delete(key)
