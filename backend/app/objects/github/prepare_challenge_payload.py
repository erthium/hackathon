from pydantic import BaseModel

from .team import Team


class PrepareChallengePayload(BaseModel):
  challenge_name: str
  teams: list[Team]
