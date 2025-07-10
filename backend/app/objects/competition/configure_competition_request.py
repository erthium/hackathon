import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class ConfigureCompetitionRequest(BaseModel):
  competition_id: UUID
  name: Optional[str] = None
  start_date: Optional[datetime.datetime] = None
  end_date: Optional[datetime.datetime] = None
  template_name: Optional[str] = None
