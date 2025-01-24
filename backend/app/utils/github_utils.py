from typing import List
import requests
from app.objects.github import GitHubHandle
from app.core.settings import app_settings

class GitHubUtils:

  @staticmethod
  def create_repository(owner_name: str, repo_name: str) -> dict:
    response = requests.post(
      "https://api.github.com/repos/ituai-deneme/deneme2/generate",
      json={
        "owner": owner_name,
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


  @staticmethod
  def create_repository_from_template(owner_name: str, repo_name: str, template_owner: str, template_repo: str) -> dict:
    response = requests.post(
      f"https://api.github.com/repos/{template_owner}/{template_repo}/generate",
      json={
        "owner": owner_name,
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


  @staticmethod
  def invite_collaborator_to_repository(owner_name: str, repo_name: str, collaborator: GitHubHandle) -> dict:
    response = requests.put(  # noqa: F841
      f"https://api.github.com/repos/{owner_name}/{repo_name}/collaborators/{collaborator}",
      headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
      },
    )

    return response.json()


  @staticmethod
  def add_webhook_to_repository(owner_name: str, repo_name: str) -> dict:
    response = requests.post(
      f"https://api.github.com/repos/{owner_name}/{repo_name}/hooks",
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


  @staticmethod
  def check_if_repository_exists(owner_name: str, repo_name: str) -> bool:
    response = requests.get(
      f"https://api.github.com/repos/{owner_name}/{repo_name}",
      headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
      },
    )

    return response.status_code == 200