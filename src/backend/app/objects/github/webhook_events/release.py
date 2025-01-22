from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field

from .common import (
  InstallationLite,
  Organization,
  Release,
  ReleaseWithPublishedAt,
  Repository,
  User,
)


class ReleaseCreatedEvent(BaseModel):
  action: Literal["created"]
  release: Release
  repository: Repository
  sender: User
  installation: InstallationLite | None = None
  organization: Organization | None = None


class ReleasePublishedEvent(BaseModel):
  action: Literal["published"]
  release: ReleaseWithPublishedAt
  repository: Repository
  sender: User
  installation: InstallationLite | None = None
  organization: Organization | None = None


class ReleaseReleasedEvent(BaseModel):
  action: Literal["released"]
  release: Release
  repository: Repository
  sender: User
  installation: InstallationLite | None = None
  organization: Organization | None = None


ReleaseEvent: TypeAlias = Annotated[
  ReleaseCreatedEvent | ReleasePublishedEvent | ReleaseReleasedEvent,
  Field(discriminator="action"),
]
