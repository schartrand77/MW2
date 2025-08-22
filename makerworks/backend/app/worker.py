import rq
from redis import Redis

from .config import settings

queue = rq.Queue(connection=Redis.from_url(settings.redis_url))

if __name__ == "__main__":
    worker = rq.Worker([queue])
    worker.work()
