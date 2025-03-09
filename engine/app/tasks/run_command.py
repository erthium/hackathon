import uuid
from urllib.parse import urljoin

import httpx
from typing import List


from app.commands import run_sandbox
from app.objects.engine import RunEngineResponse
from app.objects.template import Template, Command
from app.core.settings import app_settings


async def run_command(template: Template, command: Command, args: List[str]) -> None:
  result = await run_sandbox(template, command, args)
  fake_id = uuid.uuid4()
  engine_response = RunEngineResponse(id=fake_id, data=result)
  notify_url = urljoin(app_settings.BACKEND_BASE_URL, "engine/result")
  backend_response = httpx.post(
    notify_url,
    json=engine_response.model_dump(
      mode="json"
    ),  # mode="json" is required for UUID serialization
  )
  print(backend_response.content, flush=True)
