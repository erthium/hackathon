from fastapi import FastAPI

from app.dependencies import RateLimitDep
from app.lifespan import lifespan
from app.routers import (
  user_router,
  team_router,
  competition_router,
  invitation_router,
  release_router,
  github_router,
)


app = FastAPI(
  lifespan=lifespan,
  dependencies=[RateLimitDep]
)

app.include_router(user_router.router)
app.include_router(team_router.router)
app.include_router(competition_router.router)
app.include_router(invitation_router.router)
app.include_router(release_router.router)
app.include_router(github_router.router)


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V" # V for Vendetta
