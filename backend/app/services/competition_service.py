import datetime
from uuid import UUID
from typing import List, Optional


import requests
from app.core.settings import app_settings
from app.dependencies.database import DatabaseDep
from app.entities import Competition, Team
from app.objects.competition import (
  NecessaryTeamInfo,
  NecessaryUserInfo,
  CompetitionInfo,
  CreateCompetitionResponse,
  GetAllResponse,
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
from app.utils import GitHubUtils
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
    self, name: str, start_date: Optional[datetime.datetime], end_date: Optional[datetime.datetime]
  ) -> MessageResponse:
    # ? What about this?
    new_competition = self.__competition_repository.create(
      name=name,
      start_date=start_date,
      end_date=end_date,
    )
    return CreateCompetitionResponse(competitions_id=new_competition.id)


  def configure(
    self,
    competition_id: UUID,
    name: Optional[str] = None,
    start_date: Optional[datetime.datetime] = None,
    end_date: Optional[datetime.datetime] = None,
    template_name: Optional[str] = None,
  ) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(competition_id)
    if competition is None:
      return HTTPException(
        status_code=404, detail="Competition not found"
      )

    if name is not None:
      competition.name = name
    if start_date is not None:
      competition.start_date = start_date
    if end_date is not None:
      competition.end_date = end_date
    if template_name is not None:
      competition.template_name = template_name

    self.__competition_repository.save(competition)
    return MessageResponse(message="Competition configured successfully")



  def add_teams(self, competition_id: UUID, teams: List[NecessaryTeamInfo]) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(competition_id)

    # Ensuring the competition exists is useful for the rest
    if competition is None:
      return MessageResponse(message="Competition not found")

    # Check if all the GitHub accounts exist
    non_existent_github_accounts: List[NecessaryUserInfo] = []
    for team in teams:
      for user in team.members:
        if not self.__check_if_github_account_exist(user.github_username):
          non_existent_github_accounts.append(user)
    if len(non_existent_github_accounts) > 0:
      return MessageResponse(
        message=f"The following GitHub accounts do not exist: {'\n,'.join([f'{user.github_username} - {user.email}' for user in non_existent_github_accounts])}"
      )

    # Create teams and add users to the teams
    for team in teams:
      team_entity = self.__team_repository.create(competition.id, team.name)
      for user in team.members:
        self.__user_repository.create(
          team_entity.id, competition.id, user.github_username, user.email
        )

    return MessageResponse(message="Teams added successfully")


  def __check_if_github_account_exist(self, github_username) -> bool:
    # brkdnmz: Nice :D Nothing interesting but found it cute
    response = requests.get(f"https://api.github.com/users/{github_username}")
    return response.status_code == 200


  def start(
    self, competition_id: UUID, template_repository_owner: str, template_repository_name: str
  ) -> MessageResponse | HTTPException:
    self.__validate_template_repository(
      template_repository_owner,
      template_repository_name,
    )
    competition = self.__competition_repository.get_by_id(
      competition_id
    )

    if competition is None:
      return HTTPException(
        status_code=404, detail="Competition not found"
      )

    self.__check_if_competition_can_start(competition)

    competition.status = CompetitionStatus.ONGOING
    self.__competition_repository.save(competition)
    all_teams = self.__team_repository.get_all_by_competition_id(competition.id)
    team_action_errors: dict = {}
    for team in all_teams:
      errors = self.__create_repo_for_team(
        team,
        competition,
        template_repository_owner,
        template_repository_name,
      )
      if len(errors) > 0:
        team_action_errors[team.name] = errors

    if len(team_action_errors) > 0:
      entire_error_message = "\n".join(
        [
          f"Team: {team_name}\nErrors: {', '.join(errors)}"
          for team_name, errors in team_action_errors.items()
        ]
      )
      return HTTPException(
        status_code=400,
        detail=f"Failed to start the competition properly for the following teams:\n{entire_error_message}",
      )

    return MessageResponse(message="Competition started successfully")


  def __check_if_competition_can_start(self, competition: Competition) -> None:
    if competition.status != CompetitionStatus.UPCOMING:
      raise HTTPException(
        status_code=400, detail="Competition cannot be started, it is not in the CREATED state"
      )
    if competition.template_name is None:
      raise HTTPException(
        status_code=400, detail="Competition template is not set, please set it before starting the competition"
      )
    if competition.template is None:
      raise HTTPException(
        status_code=400, detail="Competition template is set but not found, please set an existing template"
      )


  def __validate_template_repository(
    self, template_repository_owner: str, template_repository_name: str
  ) -> None:
    does_repository_exist = GitHubUtils.check_if_repository_exists(
      template_repository_owner, template_repository_name
    )
    if not does_repository_exist:
      raise HTTPException(
        status_code=400, detail="Template repository does not exist or is private"
      )


  def __create_repository_name(self, competition: Competition, team: Team) -> str:
    return f"{competition.name}-{team.name}"


  def __create_repo_for_team(
    self,
    team: Team,
    competition: Competition,
    template_repository_owner: str,
    template_repository_name: str,
  ) -> List:
    errors: List = []

    # Create the repository
    team_repository_name = self.__create_repository_name(competition, team)
    response = GitHubUtils.create_repository_from_template(
      owner_name=template_repository_owner,
      repo_name=team_repository_name,
      template_owner=template_repository_owner,
      template_repo=template_repository_name,
    )
    if response.status_code != 200 and response.status_code != 201:
      print("For creating repostiory: ", response.status_code, response.content)
      errors.append(f"Failed to create repository '{team_repository_name}'")
    else:
      team.github_repo = team_repository_name
      self.__team_repository.save(team)

    # Send invitations to the team members
    team_members: List[str] = [user.github_username for user in team.members]
    failed_invitations: List[str] = []
    for member in team_members:
      response = GitHubUtils.invite_collaborator_to_repository(
        owner_name=template_repository_owner,
        repo_name=team_repository_name,
        collaborator=member,
      )
      if response.status_code != 200 and response.status_code != 201:
        print("For invitations: ", response.status_code, response.content)
        failed_invitations.append(member)
    for member in failed_invitations:
      errors.append(
        f"Failed to invite the team member '{member}' to the repository '{team_repository_name}'"
      )

    # Save the repository name to the team
    team.github_repo = team_repository_name
    self.__team_repository.save(team)

    # Add webhook to the repository
    response = GitHubUtils.add_webhook_to_repository(
      owner_name=template_repository_owner,
      repo_name=team_repository_name,
    )
    if response.status_code != 200 and response.status_code != 201:
      print("For Webhook: ", response.status_code, response.content)
      errors.append(f"Failed to add webhook to the repository '{team_repository_name}'")

    return errors


  def finish(
    self, competition_id: UUID
  ) -> MessageResponse:
    competition = self.__competition_repository.get_by_id(
      competition_id
    )
    if competition is None:
      return MessageResponse(message="Competition not found")

    competition.status = CompetitionStatus.COMPLETED
    self.__competition_repository.save(competition)
    # TODO: Start the evaluation process
    return MessageResponse(message="Competition finished successfully. Evaluation process may take some time.")


def get_competition_service(db: DatabaseDep) -> CompetitionService:
  return CompetitionService(
    get_competition_repository(db),
    get_team_repository(db),
    get_user_repository(db),
    get_invitation_repository(db),
  )
