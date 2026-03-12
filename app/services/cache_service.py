import redis
import json
from app.config import REDIS_HOST, REDIS_PORT, CACHE_TTL

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cache(key: str):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key: str, value):
    r.setex(key, CACHE_TTL, json.dumps(value))