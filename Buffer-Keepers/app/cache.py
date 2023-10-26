import os

import redis


def get_cache():

    # redis_url = f"redis://{os.environ.get('REDISUSER')}:{os.environ.get('REDISPASSWORD')}@{os.environ.get('REDISHOST')}:{}"
    try:
        r = redis.Redis(
            host=os.environ.get("REDISHOST"),
            port=os.environ.get("REDISPORT"),
            password=os.environ.get("REDISPASSWORD"),
            decode_responses=True,
        )
    except Exception:
        raise Exception(
            "Redis connection failed, ensure redis is running on the default port 6379"
        )
    return r


cache = get_cache()
