from typing import Annotated

from app.dependencies import TaskManagerDep
from app.tasks import run_fake_test, run_test
from fastapi import Body, FastAPI

from common.schemas import RunEnginePayload

app = FastAPI()


@app.post("/run", response_model=str)
async def run_engine(
  payload: Annotated[RunEnginePayload, Body()], task_manager: TaskManagerDep
) -> str:
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
