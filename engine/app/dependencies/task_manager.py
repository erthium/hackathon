from fastapi import Depends
from typing import Annotated

from app.services import TaskManager, get_task_manager


TaskManagerDep = Annotated[TaskManager, Depends(get_task_manager)]
