from fastapi import FastAPI

from app.dependencies import RateLimitDep
from app.lifespan import lifespan
from app import engine, github

app = FastAPI(lifespan=lifespan, dependencies=[RateLimitDep])

app.include_router(github.github_router)
app.include_router(engine.router)  # TODO: This is also rate limited, but should it be?


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V" # V for Vendetta
