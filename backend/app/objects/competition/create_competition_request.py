import datetime
from typing import Optional
from pydantic import BaseModel


class CreateCompetitionRequest(BaseModel):
  name: str
  start_date: Optional[datetime.datetime] = None
  end_date: Optional[datetime.datetime] = None
