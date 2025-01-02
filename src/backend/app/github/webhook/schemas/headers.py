from typing import Literal

from pydantic import BaseModel, Field


class WebhookHeaders(BaseModel):
  x_github_hook_id: int
  x_github_event: Literal["ping", "repository", "push", "release"]
  x_github_delivery: str
  x_hub_signature: str | None = None
  x_hub_signature_256: str | None = None
  user_agent: str = Field(pattern="^GitHub-Hookshot/.*$")
  x_github_hook_installation_target_type: str
  x_github_hook_installation_target_id: int
