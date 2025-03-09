from typing import Annotated
from fastapi import Body, APIRouter

from app.dependencies import (
  TaskManagerDep,
  TemplateServiceDep,
  CommandServiceDep
)
from app.objects.engine import RunEnginePayload
from app.tasks import run_command


router = APIRouter(prefix="/engine")


@router.post("/run", response_model=str)
async def run_engine(
  payload: Annotated[RunEnginePayload, Body()],
  task_manager: TaskManagerDep,
  template_service: TemplateServiceDep,
  command_service: CommandServiceDep
) -> str:
  template = template_service.get_template_by_name(payload.template_name)
  command = command_service.validate_and_get_command(template, payload.command, payload.args)
  task_manager.enqueue_task(
    lambda: run_command(template, command, payload.args)
  )

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