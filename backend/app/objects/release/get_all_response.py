from pydantic import BaseModel
from typing import List

from app.objects.competition.competition_info import CompetitionInfo


class GetAllResponse(BaseModel):
  competitions: List[CompetitionInfo]
