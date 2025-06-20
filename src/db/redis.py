import redis
from configuration import conf

redis_client = redis.Redis(
    host=conf.redis,
    port=conf.redis_port,
    db=conf.redis_db,
    password=conf.redis_password,
)