from pydantic import BaseModel

from .github_handle import GitHubHandle


class Team(BaseModel):
  team_name: str
  team_members: list[GitHubHandle]
