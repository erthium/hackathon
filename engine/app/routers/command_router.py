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
    id = run_command_request.submission_id
    template = template_service.get_template_by_name(run_command_request.template_name)
    command = command_service.validate_and_get_command(template, run_command_request.command, run_command_request.args)
    task_manager.enqueue_task(
      lambda: run_command(id, template, command, run_command_request.args)
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