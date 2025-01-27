import datetime
from typing import Annotated, Any
from urllib.parse import urljoin

import httpx
from app.core.settings import app_settings
from app.dependencies.release_service import release_service_dep
from app.dependencies.team_service import team_service_dep
from app.logger import logger
from app.objects.engine import TestPayload
from app.objects.github import WebhookHeaders
from app.objects.github.webhook_events import PushEvent
from fastapi import APIRouter, Body, Header

router = APIRouter(
  prefix="/github",
  tags=["github"],
)


@router.post(
  "/webhook",
  description="Handle GitHub webhook delivery",
  response_model=None,
)
async def handle_webhook_delivery(
  event: Annotated[Any, Body()],
  headers: Annotated[WebhookHeaders, Header()],
  team_service: team_service_dep,
  release_service: release_service_dep,
) -> None:
  event_type = headers.x_github_event
  logger.info(f"Received {event_type} event")

  match event_type:
    case "push":
      push_event = PushEvent.model_validate(event)

      # Test those commits that are tagged prefixed with "release"
      if not push_event.ref.startswith("refs/tags/release"):
        return

      repo_name = push_event.repository.name
      commit_id = push_event.after

      pusher_team = team_service.get_by_github_repo(repo_name)

      if not pusher_team:
        logger.warning(f"Team not found for repo {repo_name}")
        return

      # Apparently, no trusty way to get the timestamp from the event
      submission_date = datetime.datetime.now()

      submission = release_service.create(
        team_id=pusher_team.id,
        commit_id=commit_id,
        release_date=submission_date,
      )

      engine_payload = TestPayload(
        type="test",
        id=submission.id,
        repo_owner="ituai-deneme",
        repo_name=repo_name,
        commit_id=commit_id,
      )
      engine_response = httpx.post(
        urljoin(app_settings.ENGINE_API_BASE_URL, "/run"),
        json=engine_payload.model_dump(
          mode="json",  # for UUID serialization
        ),
      )
      print(engine_response.json())
    case _:
      logger.warning(f"Ignoring {event_type} event")
