from app import routers
from app.dependencies.rate_limit import RateLimitDep
from app.lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan, dependencies=[RateLimitDep])

app.include_router(routers.competition_router)
app.include_router(routers.invitation_router)
app.include_router(routers.user_router)
app.include_router(routers.team_router)
app.include_router(routers.release_router)
app.include_router(routers.template_router)
app.include_router(routers.github_router)
app.include_router(routers.engine_router)


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V"  # V for Vendetta
