from app import github
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .dependencies import RateLimitDep
from .lifespan import lifespan

app = FastAPI(lifespan=lifespan, dependencies=[RateLimitDep])

app.include_router(github.github_router)


@app.get("/", response_class=HTMLResponse)
async def root():
  return """
    <a href="/redoc">redoc</a>
    <a href="/openapi.json">redoc</a>
"""


# from sqlalchemy import text

# from .db import engine

# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())
