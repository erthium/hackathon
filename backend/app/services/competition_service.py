import requests
from typing import List, Dict
from fastapi import HTTPException

from app.entities import Competition, Team
from app.repositories import (
  CompetitionRepository, get_competition_repository,
  TeamRepository, get_team_repository,
  UserRepository, get_user_repository,
  InvitationRepository, get_invitation_repository,
)
from app.dependencies import database_dep
from app.core.settings import app_settings

from app.objects.competition import (
  GetAllResponse,
  CompetitionInfo,
  CreateCompetitionRequest,
  AddTeamsRequest, NecessaryTeamInfo, NecessaryUserInfo,
  StartCompetitionRequest,
  FinishCompetitionRequest,
)
from app.objects.message_response import MessageResponse
from app.objects.enums import CompetitionStatus

from app.utils import GitHubUtils

class CompetitionService:
  def __init__(self, 
               competition_repository: CompetitionRepository,
               team_repository: TeamRepository, 
               user_repository: UserRepository,
               invitation_repository: InvitationRepository
              ):
    self.__competition_repository = competition_repository
    self.__team_repository = team_repository
    self.__user_repository = user_repository
    self.__invitation_repository = invitation_repository

  def get_all(self) -> GetAllResponse:
    all_competitions = self.__competition_repository.get_all()
    return GetAllResponse(
      competitions=[CompetitionInfo.from_entity(competition) for competition in all_competitions]
    )


  def create(self, create_competition_request: CreateCompetitionRequest) -> MessageResponse:
    competition = Competition(
      name=create_competition_request.name,
    )
    self.__competition_repository.create(competition)
    return MessageResponse(message="Competition created successfully")


  def add_teams(self, add_teams_request: AddTeamsRequest) -> MessageResponse:
    competition = self.__competition_repository.get(add_teams_request.competition_id)

    # Check if all the GitHub accounts exist
    non_existent_github_accounts: List[NecessaryUserInfo] = []
    for team in add_teams_request.teams:
      for user in team.members:
        if not self.__check_if_github_account_exist(user.github_username):
          non_existent_github_accounts.append(user)
    if len(non_existent_github_accounts) > 0:
      return MessageResponse(message=f"The following GitHub accounts do not exist: {'\n,'.join([f'{user.github_username - {user.email}}' for user in non_existent_github_accounts])}\n\n Aborting the operation") 

    # Create teams and add users to the teams
    for team in add_teams_request.teams:
      team_entity = self.__team_repository.create(competition.id, team.name)
      for user in team.members:
        self.__user_repository.create(team_entity.id, team_entity.competition_id, user.github_username, user.email)


  async def __check_if_github_account_exist(self, github_username) -> bool:
    response = requests.get(f"https://api.github.com/users/{github_username}")
    return response.status_code == 200


  def start(self, start_competition_request: StartCompetitionRequest) -> MessageResponse:
    self.__validate_template_repository(
      start_competition_request.template_repository_owner,
      start_competition_request.template_repository_name
    )
    competition = self.__competition_repository.get_by_id(start_competition_request.competition_id)
    competition.status = CompetitionStatus.ONGOING
    self.__competition_repository.save(competition)
    all_teams = self.__team_repository.get_all_by_competition_id(competition.id)
    team_action_errors: Dict = {}
    for team in all_teams:
      errors = self.__create_repo_for_team(
        team,
        competition,
        start_competition_request.template_repository_owner,
        start_competition_request.template_repository_name
      )
      if len(errors) > 0:
        team_action_errors[team.name] = errors

    if len(team_action_errors) > 0:
      entire_error_message = "\n".join([f"Team: {team_name}\nErrors: {', '.join(errors)}" for team_name, errors in team_action_errors.items()])
      return HTTPException(status_code=400, detail=f"Failed to start the competition properly for the following teams:\n{entire_error_message}")

    return MessageResponse(message="Competition started successfully")


  def __validate_template_repository(self, template_repository_owner: str, template_repository_name: str) -> None:
    does_repository_exist = GitHubUtils.check_if_repository_exists(template_repository_owner, template_repository_name)
    if not does_repository_exist:
      raise HTTPException(status_code=400, detail="Template repository does not exist or is private")


  def __create_repository_name(self, competition: Competition, team: Team) -> str:
    return f"{competition.name}-{team.name}"


  def __create_repo_for_team(self, team: Team, competition: Competition, template_repository_owner: str, template_repository_name: str) -> List:
    errors: List = []

    # Create the repository
    team_repository_name = self.__create_repository_name(competition, team)
    response = GitHubUtils.create_repository_from_template(
      owner_name=app_settings.GITHUB_ORGANIZATION_NAME,
      repo_name=team_repository_name,
      template_owner=template_repository_owner,
      template_name=template_repository_name,
    )
    if response.status_code != 200 or response.status_code != 201:
      errors.append(f"Failed to create repository '{team_repository_name}'")
    
    # Send invitations to the team members
    team_members: List[str] = [user.github_username for user in team.members]
    failed_invitations: List[str] = []
    for member in team_members:
      response = GitHubUtils.invite_collaborator_to_repository(
        owner_name=app_settings.GITHUB_ORGANIZATION_NAME,
        repo_name=team_repository_name,
        collaborator=member,
      )
      if response.status_code != 200 or response.status_code != 201:
        failed_invitations.append(member)
    for member in failed_invitations:
      errors.append(f"Failed to invite the team member '{member}' to the repository '{team_repository_name}'")


    # Save the repository name to the team
    team.github_repo = team_repository_name
    self.__team_repository.save(team)

    # Add webhook to the repository
    response = GitHubUtils.add_webhook_to_repository(
      owner_name=app_settings.GITHUB_ORGANIZATION_NAME,
      repo_name=team_repository_name,
    )
    if response.status_code != 200 or response.status_code != 201:
      errors.append(f"Failed to add webhook to the repository '{team_repository_name}'")


  def finish(self, finish_competition_request: FinishCompetitionRequest) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(finish_competition_request.competition_id)
    competition.status = CompetitionStatus.FINISHED
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
