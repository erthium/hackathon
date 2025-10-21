from typing import List, Dict, Literal, Annotated
from pydantic import BaseModel, Field


class CommandSuccessResult(BaseModel):
  success: Literal[True] = True
  scores: Dict[str, float] = {}
  warning: List[str] = []


class CommandFailResult(BaseModel):
  success: Literal[False] = False
  error: str
  warning: List[str] = []


type CommandResult = Annotated[
  CommandSuccessResult | CommandFailResult, Field(discriminator="success")
]
