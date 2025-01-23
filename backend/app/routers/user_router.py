from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.dependencies.user_service import user_service_dep

router = APIRouter(
  prefix="/user",
  tags=["user"],
)
