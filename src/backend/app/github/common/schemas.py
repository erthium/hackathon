from pydantic import BaseModel

GitHubHandle = str


class Team(BaseModel):
    team_name: str
    team_members: list[GitHubHandle]
