from pydantic import BaseModel

from ..common.schemas import Team


class PrepareChallengePayload(BaseModel):
  challenge_name: str
  teams: list[Team]
