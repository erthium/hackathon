from pydantic import BaseModel

from .common import Commit, Committer, InstallationLite, Organization, Repository, User


class PushEvent(BaseModel):
  ref: str
  before: str
  after: str
  created: bool
  deleted: bool
  forced: bool
  base_ref: str | None
  compare: str
  commits: list[Commit]
  head_commit: Commit | None
  repository: Repository
  pusher: Committer
  sender: User
  installation: InstallationLite | None = None
  organization: Organization | None = None
