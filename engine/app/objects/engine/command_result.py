from typing import List, Literal, Annotated
from pydantic import BaseModel, Field


class CommandSuccessResult(BaseModel):
  success: Literal[True] = True
  scores: List[float]
  warning: List[str] = []


class CommandFailResult(BaseModel):
  success: Literal[False] = False
  error: str
  Warning: List[str] = []


type CommandResult = Annotated[
  CommandSuccessResult | CommandFailResult, Field(discriminator="success")
]
