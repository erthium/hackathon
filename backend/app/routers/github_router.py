import httpx
from typing import Annotated, Any
from urllib.parse import urljoin
from fastapi import APIRouter, Body, Header, Request

from app.logger import logger
from app.core.settings import app_settings
from app.objects.engine import RunCommandRequest
from app.objects.github import WebhookHeaders
from app.objects.github.webhook_events import PushEvent
from app.objects.enums import RunCommandType
from app.dependencies.team_service import TeamServiceDep
from app.dependencies.release_service import ReleaseServiceDep
from app.dependencies.template_service import TemplateServiceDep
from app.utils import GitHubUtils, TemplateUtils

router = APIRouter(prefix="/github", tags=["webhook"])


@router.post(
  "/webhook",
  summary="GitHub webhook delivery endpoint",
  description="Handles GitHub webhook events, specifically push events for releases. Not to be used directly by users.",
)
async def handle_webhook_delivery(
  request: Request,
  event: Annotated[Any, Body()], 
  headers: Annotated[WebhookHeaders, Header()],
  team_service: TeamServiceDep,
  release_service: ReleaseServiceDep,
  template_service: TemplateServiceDep,
) -> None:
  event_type = headers.x_github_event
  logger.info(f"Received {event_type} event")
  match event_type:
    case "push":
      push_event = PushEvent.model_validate(event)
      repo_name = push_event.repository.name

      GitHubUtils.verify_github_signature_from_webhook(
        repo_name=repo_name,
        payload_body=await request.body(),
        signature_header=headers.x_hub_signature_256,
      )
      
      logger.info(f"Received webhook event for repository: {repo_name} with signature: {headers.x_hub_signature_256}")

      if push_event.head_commit.message.startswith("release"):
        team = team_service.get_team_by_repo(push_event.repository.name)
        command_run = release_service.create_command_run_by_push_event(team.id, push_event)
        template = team.competition.template

        if template.on_submission_command is None:
          logger.warning(
            f"Template {template.name} does not have an on_submission_command defined. "
            "Skipping engine command execution."
          )
          return

        command = template_service.get_command_from_type(template, RunCommandType.ON_SUBMISSION)

        if command is None:
          logger.warning(
            f"Template {template.name} does not have an on_submission_command defined. "
            "Skipping engine command execution."
          )
          return

        # For the ON_SUBMISSION command, we pass the repository full name as an argument
        # For now, there is no other possibility than "arg_type" being anything but "SENDER_REPO"
        repo_owner = push_event.repository.owner.login
        commit_id = push_event.head_commit.id
        repo_arg = TemplateUtils.repo_args_to_str(
          repo_owner=repo_owner,
          repo_name=repo_name,
          commit_id=commit_id,
        )
        args = [repo_arg,]

        engine_payload = RunCommandRequest(
          command_run_id=command_run.id,
          run_command_type=RunCommandType.ON_SUBMISSION,
          template_name=template.name,
          command_name=command.name,
          args=args,
        )

        engine_response = httpx.post(
          urljoin(app_settings.ENGINE_API_BASE_URL, "/command/run"),
          json=engine_payload.model_dump(
            mode="json",  # for UUID serialization
          ),
        )
        logger.info(f"Engine response: {engine_response.content}")
    case _:
      logger.warning(f"Ignoring {event_type} event, which should not even be received by this endpoint.")
