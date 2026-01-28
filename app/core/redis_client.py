import redis
import os

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

redis_client.set("test", "hello")
print(redis_client.get("test"))