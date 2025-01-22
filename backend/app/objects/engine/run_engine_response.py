import uuid

from pydantic import BaseModel

from .engine_result import EngineTestResult


class RunEngineResponse(BaseModel):
  id: uuid.UUID  # Database ID type
  data: EngineTestResult
