from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.dependencies.team_service import TeamServiceDep

router = APIRouter(
  prefix="/team",
  tags=["team"],
)
