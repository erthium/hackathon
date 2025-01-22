import uuid
from typing import Annotated, Any
from urllib.parse import urljoin

import httpx
from app.db import app_settings
from app.logger import logger
from fastapi import APIRouter, Body, Header

from common.schemas import TestPayload

from .schemas import PushEvent, WebhookHeaders

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def handle_webhook_delivery(
  event: Annotated[Any, Body()], headers: Annotated[WebhookHeaders, Header()]
) -> None:
  event_type = headers.x_github_event
  logger.info(f"Received {event_type} event")

  match event_type:
    case "push":
      push_event = PushEvent.model_validate(event)

      # Test those commits that are tagged prefixed with "release"
      if push_event.ref.startswith("refs/tags/release"):
        fake_id = uuid.uuid4()
        engine_payload = TestPayload(
          id=fake_id,
          type="test",
          repo_owner="ituai-deneme",
          repo_name=push_event.repository.name,
          commit_id=push_event.after,
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
