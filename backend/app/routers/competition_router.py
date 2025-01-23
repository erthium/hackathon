from fastapi import APIRouter, HTTPException, status, Request
import traceback

from app.objects.competition import (
  GetAllResponse,
  CreateCompetitionRequest,
  AddTeamsRequest,
  StartCompetitionRequest,
  FinishCompetitionRequest,
)
from app.objects.message_response import MessageResponse

from app.dependencies.competition_service import competition_service_dep
from utils.ErrorUtils import ErrorUtils

router = APIRouter(
  prefix="/competition",
  tags=["competition"],
)

@router.get(
  "/all",
  description="Get all competitions",
  response_description="List of competitions",
)
async def get_all_competitions(request: Request, competition_service: competition_service_dep) -> GetAllResponse:
  try:
    return await competition_service.get_all()
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/create",
  description="Create a competition with the team and user information",
)
async def create_competition(request: Request, createCompetitionRequest: CreateCompetitionRequest, competition_service: competition_service_dep):
  try:
    return await competition_service.create(createCompetitionRequest)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/add_teams",
  description="Add teams to a competition",
)
async def add_teams(request: Request, addTeamsRequest: AddTeamsRequest, competition_service: competition_service_dep):
  try:
    return await competition_service.add_teams(addTeamsRequest)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/start",
  description="Start a competition",
)
async def start_competition(request: Request, startCompetitionRequest: StartCompetitionRequest, competition_service: competition_service_dep):
  try:
    return await competition_service.start(startCompetitionRequest)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)