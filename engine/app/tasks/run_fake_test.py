import uuid
from urllib.parse import urljoin

import httpx
from app.commands import fake_test
from app.objects.engine import RunEngineResponse
from app.settings import app_settings


async def run_fake_test() -> None:
  result = await fake_test()
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
