from typing import Literal, TypeAlias

from pydantic import BaseModel

from .common import InstallationLite, Organization, Repository, User


class RepositoryCreatedEvent(BaseModel):
  action: Literal["created"]
  repository: Repository
  sender: User
  installation: InstallationLite | None = None
  organization: Organization | None = None


RepositoryEvent: TypeAlias = RepositoryCreatedEvent
