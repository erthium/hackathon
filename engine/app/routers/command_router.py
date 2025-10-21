import traceback
from typing import Annotated
from fastapi import Body, APIRouter

from app.dependencies import (
  TaskManagerDep,
  TemplateServiceDep,
  CommandServiceDep
)
from app.objects.engine import RunCommandRequest
from app.objects import MessageResponse
from app.tasks import run_command
from app.utils import ErrorUtils

router = APIRouter(prefix="/command", tags=["Command"])


@router.post(
  "/run",
  response_model=MessageResponse,
  summary="Run a command on a template",
)
async def run_engine(
  run_command_request: Annotated[RunCommandRequest, Body()],
  task_manager: TaskManagerDep,
  template_service: TemplateServiceDep,
  command_service: CommandServiceDep
) -> MessageResponse:
  try:
    command_run_id = run_command_request.command_run_id
    run_command_type = run_command_request.run_command_type
    template_name = run_command_request.template_name
    command_name = run_command_request.command_name
    args = run_command_request.args
    print(f"For submission with ID '{command_run_id}' running command {command_name} on template {template_name} with args {args}", flush=True)
    template = template_service.get_template_by_name(template_name)
    command = command_service.validate_and_get_command(template, command_name, args)
    task_manager.enqueue_task(
      lambda: run_command(command_run_id, run_command_type, template, command, args)
    )
    return MessageResponse(message="Command running process started successfully")
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)

  """
  match payload.type:
    case "test":
      task_manager.enqueue_task(
        lambda: run_test(payload.repo_owner, payload.repo_name, payload.commit_id)
      )
      return "Results will be sent soon"
    case "evaluate":
      return "Evaluation is not supported yet"
    case "fake_test":
      task_manager.enqueue_task(run_fake_test)
      return "Results will be sent soon"
    case _:
      return "Unknown payload type"
  """