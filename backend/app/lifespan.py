from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from app.core.settings import app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
  redis_connection = redis.from_url(
    app_settings.REDIS_URL,
    password=app_settings.REDIS_PASSWORD,
    encoding="utf-8",
    decode_responses=True,
  )
  await FastAPILimiter.init(redis_connection)
  yield
