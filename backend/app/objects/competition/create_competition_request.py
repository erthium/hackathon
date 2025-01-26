import datetime

from pydantic import BaseModel


class CreateCompetitionRequest(BaseModel):
  name: str
  start_date: datetime.datetime
  end_date: datetime.datetime
