from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from .settings import app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url(
        app_settings.redis_url,
        password=app_settings.redis_password,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_connection)
    yield
