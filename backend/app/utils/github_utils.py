import hmac
import hashlib
import requests
from fastapi import HTTPException

from app.core.settings import app_settings
from app.objects.github import GitHubHandle
from app.objects.github.webhook_events import PushEvent
from app.objects.github import WebhookHeaders


class GitHubUtils:
  @staticmethod
  def generate_secret_token_for_webhook(repo_name: str) -> str:
    """
    Creates a salted secret key for the GitHub repository.
    The salt is the repository name, and the key is the GitHub PAT token.
    """
    return f"{repo_name}:{app_settings.GITHUB_SECRET_TOKEN}:{repo_name}"


  @staticmethod
  def verify_github_signature_from_webhook(repo_name: str, payload_body: any, signature_header: str) -> None:
    """
    Validates the secret key for the GitHub repository.
    The salt is the repository name, and the key is the GitHub PAT token.
    """
    if not signature_header:
      raise HTTPException(
        status_code=403,
        detail="You really should not be here"
      )

    secret_token = GitHubUtils.generate_secret_token_for_webhook(repo_name)
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
      print(f"Expected signature: {expected_signature}, received signature: {signature_header}")
      """
      raise HTTPException(
        status_code=403,
        detail="We know you are trying as hard as you can, but you are both not allowed and not smart enough to do this pal..."
      )
      """
    print(f"Signature verified successfully! Expected: {expected_signature}, received: {signature_header}")

  @staticmethod
  def create_repository(owner_name: str, repo_name: str) -> requests.Response:
    github_owner = app_settings.GITHUB_OWNER
    response = requests.post(
      f"https://api.github.com/repos/{github_owner}/{repo_name}/generate",
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
    return response


  @staticmethod
  def create_repository_from_template(
    owner_name: str, repo_name: str, template_owner: str, template_repo: str
  ) -> requests.Response:
    print(f"PAT Token: {app_settings.GITHUB_PAT_TOKEN}")
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
    return response


  @staticmethod
  def invite_collaborator_to_repository(
    owner_name: str, repo_name: str, collaborator: GitHubHandle
  ) -> requests.Response:
    response = requests.put(  # noqa: F841
      f"https://api.github.com/repos/{owner_name}/{repo_name}/collaborators/{collaborator}",
      headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
      },
    )

    return response


  @staticmethod
  def add_webhook_to_repository(owner_name: str, repo_name: str) -> requests.Response:
    response = requests.post(
      f"https://api.github.com/repos/{owner_name}/{repo_name}/hooks",
      json={
        "name": "web",
        "active": True,
        "events": ["push"],
        "config": {
          "url": f"{app_settings.WEBHOOK_URL}/github/webhook",
          "content_type": "json",
          "secret": GitHubUtils.generate_secret_token_for_webhook(repo_name),
        },
      },
      headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_settings.GITHUB_PAT_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
      },
    )

    return response


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
