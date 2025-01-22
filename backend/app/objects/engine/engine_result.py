from typing import Annotated, Literal

from pydantic import BaseModel, Field


class EngineTestSucceededResult(BaseModel):
  success: Literal[True] = True
  result: str


class EngineTestFailedResult(BaseModel):
  success: Literal[False] = False
  error: str


EngineTestResult = Annotated[
  EngineTestSucceededResult | EngineTestFailedResult, Field(discriminator="success")
]
