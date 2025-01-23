from pydantic import BaseModel


class CreateCompetitionRequest(BaseModel):
  name: str
  