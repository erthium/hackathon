import traceback
from uuid import UUID

from app.dependencies.competition_service import CompetitionServiceDep
from app.objects.competition import (
  AddTeamsRequest, NecessaryTeamInfo, NecessaryUserInfo,
  CreateCompetitionRequest,
  CreateCompetitionResponse,
  ConfigureCompetitionRequest,
  GetAllResponse,
  StartCompetitionRequest,
  FinishCompetitionRequest,
)
from app.objects.message_response import MessageResponse
from app.utils.error_utils import ErrorUtils
from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/competition",
  tags=["competition"],
)


@router.get(
  "/all",
  description="Get all competitions",
  response_description="List of competitions",
  response_model=GetAllResponse,
)
async def get_all_competitions(
  request: Request, competition_service: CompetitionServiceDep
) -> GetAllResponse:
  try:
    return competition_service.get_all()
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/create",
  description="Create a competition with the team and user information",
  response_description="Competition information",
  response_model=CreateCompetitionResponse,
)
async def create_competition(
  request: Request,
  create_competition_request: CreateCompetitionRequest,
  competition_service: CompetitionServiceDep,
) -> CreateCompetitionResponse:
  try:
    name = create_competition_request.name
    start_date = create_competition_request.start_date
    end_date = create_competition_request.end_date
    return competition_service.create(name, start_date, end_date)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.put(
  "/configure",
  description="Configure a competition with necessary information",
  response_description="Message indicating success or failure",
  response_model=MessageResponse,
)
async def configure_competition(
  request: Request,
  configure_competition_request: ConfigureCompetitionRequest,
  competition_service: CompetitionServiceDep,
) -> MessageResponse:
  try:
    competition_id = configure_competition_request.competition_id
    name = configure_competition_request.name
    start_date = configure_competition_request.start_date
    end_date = configure_competition_request.end_date
    template_name = configure_competition_request.template_name
    return competition_service.configure(
      competition_id,
      name,
      start_date,
      end_date,
      template_name,
    )
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/add_teams",
  description="Add teams to a competition",
  response_model=MessageResponse,
)
async def add_teams(
  request: Request,
  add_teams_request: AddTeamsRequest,
  competition_service: CompetitionServiceDep,
) -> MessageResponse:
  try:
    competition_id = add_teams_request.competition_id
    teams = add_teams_request.teams
    return competition_service.add_teams(competition_id, teams)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/start",
  description="Start a competition",
  response_model=MessageResponse,
)
async def start_competition(
  request: Request,
  start_competition_request: StartCompetitionRequest,
  competition_service: CompetitionServiceDep,
) -> MessageResponse:
  try:
    competition_id = start_competition_request.competition_id
    template_repository_owner = start_competition_request.template_repository_owner
    template_repository_name = start_competition_request.template_repository_name 
    print("Start competition request:", start_competition_request)
    return competition_service.start(
      competition_id,
      template_repository_owner,
      template_repository_name,
    )
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/finish",
  description="Finish a competition",
  response_model=MessageResponse,
)
async def finish_competition(
  request: Request,
  finish_competition_request: FinishCompetitionRequest,
  competition_service: CompetitionServiceDep,
) -> MessageResponse:
  try:
    competition_id = finish_competition_request.competition_id
    return competition_service.finish(competition_id)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
