from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.dependencies.team_service import team_service_dep

router = APIRouter(
  prefix="/team",
  tags=["team"],
)
