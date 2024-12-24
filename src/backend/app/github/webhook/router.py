from typing import Annotated, Any

import requests
from app.logger import logger
from app.settings import ENGINE_API_BASE_URL
from fastapi import APIRouter, Body, Header
from pydantic import TypeAdapter

from .schemas import PushEvent, ReleaseEvent, WebhookHeaders

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def handle_webhook_delivery(
    event: Annotated[Any, Body()], headers: Annotated[WebhookHeaders, Header()]
):
    event_type = headers.x_github_event
    logger.info(f"Received {event_type} event")

    match event_type:
        case "ping":
            pass
        case "repository":
            pass
        case "push":
            push_event = PushEvent.model_validate(event)
        case "release":
            ta: TypeAdapter[ReleaseEvent] = TypeAdapter(ReleaseEvent)
            release_event = ta.validate_python(event)
            if release_event.action == "published":
                logger.info(
                    f"Release published in repository {release_event.repository.name} ({release_event.repository.html_url}): {release_event.release.name} ({release_event.release.html_url})"
                )

                try:
                    logger.info("Running engine")
                    response = requests.get(
                        f"{ENGINE_API_BASE_URL}/{release_event.repository.owner.login}/{release_event.repository.name}/releases/{release_event.release.tag_name}",
                    )
                    logger.info(response.json())
                except Exception as e:
                    logger.error(e)
        case _:
            logger.warning("Unknown webhook event")
