from app.dependencies import RateLimitDep
from app.lifespan import lifespan
from app.routers import (
  competition_router,
  engine_router,
  github_router,
  invitation_router,
  release_router,
  team_router,
  user_router,
)
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan, dependencies=[RateLimitDep])

app.include_router(user_router)
app.include_router(team_router)
app.include_router(competition_router)
app.include_router(invitation_router)
app.include_router(release_router)
app.include_router(github_router)
app.include_router(engine_router)


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V"  # V for Vendetta
