from typing import Literal

from pydantic import BaseModel, Field


class User(BaseModel):
  login: str
  id: int
  node_id: str
  name: str | None = None
  email: str | None = None
  avatar_url: str
  gravatar_id: str
  url: str
  html_url: str
  followers_url: str
  following_url: str
  gists_url: str
  starred_url: str
  subscriptions_url: str
  organizations_url: str
  repos_url: str
  events_url: str
  received_events_url: str
  type: Literal["Bot", "User", "Organization"]
  site_admin: bool


class InstallationLite(BaseModel):
  id: int
  node_id: str


class Organization(BaseModel):
  login: str
  id: int
  node_id: str
  url: str
  html_url: str | None = None
  repos_url: str
  events_url: str
  hooks_url: str
  issues_url: str
  members_url: str
  public_members_url: str
  avatar_url: str
  description: str | None


class License(BaseModel):
  key: str
  name: str
  spdx_id: str
  url: str | None
  node_id: str


class RepositoryPermissions(BaseModel):
  pull: bool
  push: bool
  admin: bool
  maintain: bool | None = None
  triage: bool | None = None


class Repository(BaseModel):
  id: int
  node_id: str
  name: str
  full_name: str
  private: bool
  owner: User
  html_url: str
  description: str | None
  fork: bool
  url: str
  forks_url: str
  keys_url: str
  collaborators_url: str
  teams_url: str
  hooks_url: str
  issue_events_url: str
  events_url: str
  assignees_url: str
  branches_url: str
  tags_url: str
  blobs_url: str
  git_tags_url: str
  git_refs_url: str
  trees_url: str
  statuses_url: str
  languages_url: str
  stargazers_url: str
  contributors_url: str
  subscribers_url: str
  subscription_url: str
  commits_url: str
  git_commits_url: str
  comments_url: str
  issue_comment_url: str
  contents_url: str
  compare_url: str
  merges_url: str
  archive_url: str
  downloads_url: str
  issues_url: str
  pulls_url: str
  milestones_url: str
  notifications_url: str
  labels_url: str
  releases_url: str
  deployments_url: str
  created_at: int | str
  updated_at: str
  pushed_at: int | str | None
  git_url: str
  ssh_url: str
  clone_url: str
  svn_url: str
  homepage: str | None
  size: int
  stargazers_count: int
  watchers_count: int
  language: str | None
  has_issues: bool
  has_projects: bool
  has_downloads: bool
  has_wiki: bool
  has_pages: bool
  has_discussions: bool | None = None
  forks_count: int
  mirror_url: str | None
  archived: bool
  disabled: bool | None = None
  open_issues_count: int
  license: License | None
  forks: int
  open_issues: int
  watchers: int
  stargazers: int | None = None
  default_branch: str
  allow_squash_merge: bool | None = None
  allow_merge_commit: bool | None = None
  allow_rebase_merge: bool | None = None
  allow_auto_merge: bool | None = None
  allow_forking: bool | None = None
  allow_update_branch: bool | None = None
  use_squash_pr_title_as_default: bool | None = None
  squash_merge_commit_message: str | None = None
  squash_merge_commit_title: str | None = None
  merge_commit_message: str | None = None
  merge_commit_title: str | None = None
  is_template: bool
  web_commit_signoff_required: bool
  topics: list[str]
  visibility: Literal["public", "private", "internal"]
  delete_branch_on_merge: bool | None = None
  master_branch: str | None = None
  permissions: RepositoryPermissions | None = None
  public: bool | None = None
  organization: str | None = None
  custom_properties: dict[str, str | list[str] | None]


class Committer(BaseModel):
  name: str
  email: str | None
  date: str | None = None
  username: str | None = None


class Commit(BaseModel):
  id: str
  tree_id: str
  distinct: bool
  message: str
  timestamp: str
  url: str
  author: Committer
  committer: Committer
  added: list[str]
  modified: list[str]
  removed: list[str]


class ReleaseAsset(BaseModel):
  url: str
  browser_download_url: str
  id: int
  node_id: str
  name: str
  label: str | None
  state: Literal["uploaded"]
  content_type: str
  size: int
  download_count: int
  created_at: str
  updated_at: str
  uploader: User | None = None


class Reactions(BaseModel):
  url: str
  total_count: int
  plus1: int = Field(..., alias="+1")
  minus1: int = Field(..., alias="-1")
  laugh: int
  hooray: int
  confused: int
  heart: int
  rocket: int
  eyes: int


class Release(BaseModel):
  url: str
  assets_url: str
  upload_url: str
  html_url: str
  id: int
  node_id: str
  tag_name: str
  target_commitish: str
  name: str
  draft: bool
  author: User
  prerelease: bool
  created_at: str | None
  published_at: str | None
  assets: list[ReleaseAsset]
  tarball_url: str | None
  zipball_url: str | None
  body: str
  mentions_count: int | None = None
  reactions: Reactions | None = None
  discussion_url: str | None = None


class ReleaseWithPublishedAt(Release):
  published_at: str
