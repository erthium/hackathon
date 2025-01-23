from app import engine, github, routers
from app.dependencies import RateLimitDep
from app.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan, dependencies=[RateLimitDep])

app.include_router(github.github_router)
app.include_router(engine.router)  # TODO: This is also rate limited, but should it be?
app.include_router(routers.competition_router)
app.include_router(routers.invitation_router)
app.include_router(routers.user_router)
app.include_router(routers.team_router)
app.include_router(routers.release_router)


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V"  # V for Vendetta
