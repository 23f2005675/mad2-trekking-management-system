import json
import redis

from config import Config

try:
    redis_client = redis.from_url(
        Config.REDIS_URL,
        decode_responses=True
    )
except Exception:
    redis_client = None


def cache_get(key):

    if redis_client is None:
        return None

    try:
        data = redis_client.get(key)

        if data:
            return json.loads(data)

    except Exception:
        pass

    return None


def cache_set(key, value, ttl=60):

    if redis_client is None:
        return

    try:
        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )
    except Exception:
        pass


def cache_delete_pattern(pattern):

    if redis_client is None:
        return

    try:
        for key in redis_client.scan_iter(pattern):
            redis_client.delete(key)
    except Exception:
        pass