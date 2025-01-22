from functools import lru_cache
from typing import Annotated

from app.tasks import TaskManager
from fastapi import Depends


@lru_cache  # to always get the same singleton TaskManager instance
def get_task_manager() -> TaskManager:
  task_manager = TaskManager(max_tasks=1)
  return task_manager


TaskManagerDep = Annotated[TaskManager, Depends(get_task_manager)]
