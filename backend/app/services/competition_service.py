from typing import List

import requests
from app.dependencies import database_dep
from app.entities import Competition, Team
from app.objects.competition import (
  AddTeamsRequest,
  CompetitionInfo,
  CreateCompetitionRequest,
  FinishCompetitionRequest,
  GetAllResponse,
  NecessaryUserInfo,
  StartCompetitionRequest,
)
from app.objects.enums import CompetitionStatus
from app.objects.message_response import MessageResponse
from app.repositories import (
  CompetitionRepository,
  InvitationRepository,
  TeamRepository,
  UserRepository,
  get_competition_repository,
  get_invitation_repository,
  get_team_repository,
  get_user_repository,
)
from fastapi import HTTPException


class CompetitionService:
  def __init__(
    self,
    competition_repository: CompetitionRepository,
    team_repository: TeamRepository,
    user_repository: UserRepository,
    invitation_repository: InvitationRepository,
  ):
    self.__competition_repository = competition_repository
    self.__team_repository = team_repository
    self.__user_repository = user_repository
    self.__invitation_repository = invitation_repository  # TODO: Currently unused

  def get_all(self) -> GetAllResponse:
    all_competitions = self.__competition_repository.get_all()
    return GetAllResponse(
      competitions=[
        CompetitionInfo.from_entity(competition) for competition in all_competitions
      ]
    )

  def create(
    self, create_competition_request: CreateCompetitionRequest
  ) -> MessageResponse:
    # ? What about this?
    self.__competition_repository.create(
      create_competition_request.name,
      create_competition_request.start_date,
      create_competition_request.end_date,
    )
    return MessageResponse(message="Competition created successfully")

  def add_teams(self, add_teams_request: AddTeamsRequest) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(
      add_teams_request.competition_id
    )

    # Ensuring the competition exists is useful for the rest
    if competition is None:
      return MessageResponse(message="Competition not found")

    # Check if all the GitHub accounts exist
    non_existent_github_accounts: List[NecessaryUserInfo] = []
    for team in add_teams_request.teams:
      for user in team.members:
        if not self.__check_if_github_account_exist(user.github_username):
          non_existent_github_accounts.append(user)
    if len(non_existent_github_accounts) > 0:
      return MessageResponse(
        message=f"The following GitHub accounts do not exist: {'\n,'.join([f'{user.github_username} - {user.email}' for user in non_existent_github_accounts])}"
      )

    # Create teams and add users to the teams
    for team in add_teams_request.teams:
      team_entity = self.__team_repository.create(competition.id, team.name)
      for user in team.members:
        self.__user_repository.create(
          team_entity.id, competition.id, user.github_username, user.email
        )

    return MessageResponse(message="Teams added successfully")

  async def __check_if_github_account_exist(self, github_username) -> bool:
    # brkdnmz: Nice :D Nothing interesting but found it cute
    response = requests.get(f"https://api.github.com/users/{github_username}")
    return response.status_code == 200

  def start(
    self, start_competition_request: StartCompetitionRequest
  ) -> MessageResponse:
    self.__validate_template_repository(
      start_competition_request.template_repository_owner,
      start_competition_request.template_repository_name,
    )
    competition = self.__competition_repository.get_by_id(
      start_competition_request.competition_id
    )

    if competition is None:
      return MessageResponse(message="Competition not found")

    competition.status = CompetitionStatus.ONGOING
    self.__competition_repository.save(competition)
    all_teams = self.__team_repository.get_all_by_competition_id(competition.id)
    for team in all_teams:
      self.__create_repo_for_team(
        team,
        competition,
        start_competition_request.template_repository_owner,
        start_competition_request.template_repository_name,
      )
    return MessageResponse(message="Competition started successfully")

  def __validate_template_repository(
    self, template_repository_owner: str, template_repository_name: str
  ) -> None:
    # This should work
    # the .git suffix may be unnecessary tho
    url = (
      f"https://github.com/{template_repository_owner}/{template_repository_name}.git"
    )
    response = requests.get(url)
    if response.status_code != 200:
      raise HTTPException(status_code=400, detail="Invalid template repository")

  def __create_repo_for_team(
    self,
    team: Team,
    competition: Competition,
    template_repository_owner: str,
    template_repository_name: str,
  ):
    pass  # TODO: Implement this method
    # Create the repository and send invitation to the team members

  def finish(
    self, finish_competition_request: FinishCompetitionRequest
  ) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(
      finish_competition_request.competition_id
    )

    if competition is None:
      return MessageResponse(message="Competition not found")

    competition.status = CompetitionStatus.COMPLETED
    self.__competition_repository.save(competition)
    # TODO: Start the evaluation process
    return MessageResponse(message="Competition finished successfully")


def get_competition_service(db: database_dep) -> CompetitionService:
  return CompetitionService(
    get_competition_repository(db),
    get_team_repository(db),
    get_user_repository(db),
    get_invitation_repository(db),
  )
