import uuid
from urllib.parse import urljoin

import httpx
from app.commands import test
from app.objects.engine import RunEngineResponse
from app.settings import app_settings


async def run_test(
  repo_owner: str, repo_name: str, commit_id: str, submission_id: uuid.UUID
) -> None:
  result = await test(repo_owner, repo_name, commit_id)
  engine_response = RunEngineResponse(id=submission_id, data=result)
  notify_url = urljoin(app_settings.BACKEND_BASE_URL, "engine/result")
  backend_response = httpx.post(
    notify_url,
    json=engine_response.model_dump(
      mode="json"
    ),  # mode="json" is required for UUID serialization
  )
  print(backend_response.content, flush=True)
