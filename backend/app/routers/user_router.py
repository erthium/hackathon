from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.dependencies.user_service import UserServiceDep

router = APIRouter(
  prefix="/user",
  tags=["user"],
)
