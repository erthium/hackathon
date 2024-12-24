from fastapi import APIRouter

from .actions.router import router as actions_router
from .webhook.router import router as webhook_router

github_router = APIRouter(prefix="/github")
github_router.include_router(webhook_router)
github_router.include_router(actions_router)
