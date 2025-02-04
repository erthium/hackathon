from typing import Annotated, Literal

from pydantic import BaseModel, Field


class EngineTestSucceededResult(BaseModel):
  success: Literal[True] = True
  result: str
  score: float  # Used for the demo, just to show this info can be returned


class EngineTestFailedResult(BaseModel):
  success: Literal[False] = False
  error: str


EngineTestResult = Annotated[
  EngineTestSucceededResult | EngineTestFailedResult, Field(discriminator="success")
]
