import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class BasePayload(BaseModel):
  id: uuid.UUID  # Database ID type
  repo_owner: str
  repo_name: str
  commit_id: str


class TestPayload(BasePayload):
  type: Literal["test"]


class EvaluatePayload(BasePayload):
  type: Literal["evaluate"]


# This does not derive from BasePayload as it does not handle repository cloning
class FakeTestPayload(BaseModel):
  type: Literal["fake_test"]


type RunEnginePayload = Annotated[
  TestPayload | EvaluatePayload | FakeTestPayload, Field(discriminator="type")
]
