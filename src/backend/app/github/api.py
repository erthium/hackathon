import requests
from app.settings import app_settings

from .common.schemas import GitHubHandle

"""
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/TEMPLATE_OWNER/TEMPLATE_REPO/generate \
  -d '{"owner":"octocat","name":"Hello-World","description":"This is your first repository","include_all_branches":false,"private":false}'
"""


def create_repo_in_org(org_name: str, repo_name: str):
  response = requests.post(
    "https://api.github.com/repos/ituai-deneme/deneme2/generate",
    json={
      "owner": org_name,
      "name": repo_name,
      "description": "",
      "include_all_branches": False,
      "private": True,
    },
    headers={
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
      "X-GitHub-Api-Version": "2022-11-28",
    },
  )

  return response.json()


def invite_collaborators_to_repo(
  org_name: str, repo_name: str, collaborators: list[GitHubHandle]
):
  for collaborator in collaborators:
    response = requests.put(  # noqa: F841
      f"https://api.github.com/repos/{org_name}/{repo_name}/collaborators/{collaborator}",
      headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
      },
    )


def add_webhook_to_repo(org_name: str, repo_name: str):
  response = requests.post(
    f"https://api.github.com/repos/{org_name}/{repo_name}/hooks",
    json={
      "name": "web",
      "active": True,
      "events": ["push"],
      "config": {
        "url": "https://imp-patient-evidently.ngrok-free.app/github/webhook",
        "content_type": "json",
      },
    },
    headers={
      "Accept": "application/vnd.github+json",
      "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
      "X-GitHub-Api-Version": "2022-11-28",
    },
  )

  return response.json()
