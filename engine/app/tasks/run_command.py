import httpx
import traceback
from urllib.parse import urljoin
from uuid import UUID
from typing import List

from app.commands import run_sandbox
from app.objects.engine import RunCommandResponse, CommandResult, CommandFailResult, CommandSuccessResult
from app.objects.template import Template, Command
from app.objects.enums import RunCommandType
from app.core.settings import app_settings


async def run_command(command_run_id: UUID, run_command_type:  RunCommandType, template: Template, command: Command, args: List[str]) -> None:
  try:
    result: CommandResult = await run_sandbox(template, command, args)
    run_command_response = None
    if isinstance(result, CommandFailResult):
      run_command_response = RunCommandResponse(
        command_run_id=command_run_id,
        run_command_type=run_command_type,
        template_name=template.name,
        command_name=command.name,
        success=result.success,
        scores=[],
        error=result.error,
      )
      notify_url = urljoin(app_settings.BACKEND_BASE_URL, "engine/result")
      backend_response = httpx.post(
        notify_url,
        json=run_command_response.model_dump(
          mode="json"
        ),  # mode="json" is required for UUID serialization
      )

    elif isinstance(result, CommandSuccessResult):
      if len(result.scores) != len(template.score_metrics):
        raise ValueError(
          f"Expected {len(template.score_metrics)} number of scores, but got {len(result.scores)}"
        )
      run_command_response = RunCommandResponse(
        command_run_id=command_run_id,
        run_command_type=run_command_type,
        template_name=template.name,
        command_name=command.name,
        success=result.success,
        scores=result.scores,
        error=None,
      )
    notify_url = urljoin(app_settings.BACKEND_BASE_URL, "engine/result")
    backend_response = httpx.post(
      notify_url,
      json=run_command_response.model_dump(
        mode="json"
      ),  # mode="json" is required for UUID serialization
    )
    print(backend_response.content, flush=True)
  except Exception as e:
    print(f"An error occurred while running the command: {e}", flush=True)
    traceback.print_exc()
    run_command_response = RunCommandResponse(
      command_run_id=command_run_id,
      run_command_type=run_command_type,
      template_name=template.name,
      command_name=command.name,
      success=False,
      scores=[],
      error=str(e),
    )
    notify_url = urljoin(app_settings.BACKEND_BASE_URL, "engine/result")
    backend_response = httpx.post(
      notify_url,
      json=run_command_response.model_dump(
        mode="json"
      ),  # mode="json" is required for UUID serialization
    )
    print(backend_response.content, flush=True)