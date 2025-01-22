import asyncio
from typing import Callable, Coroutine


class TaskManager:
  def __init__(self, max_tasks: int) -> None:
    self.task_queue: asyncio.Queue[Callable[..., Coroutine]] = asyncio.Queue(
      maxsize=max_tasks
    )
    self.worker_initiated = False

  def init_worker(self) -> None:
    asyncio.create_task(self.worker())
    self.worker_initiated = True

  def enqueue_task(self, task: Callable[..., Coroutine]) -> None:
    if not self.worker_initiated:
      self.init_worker()

    async def enqueue() -> None:
      await self.task_queue.put(task)

    asyncio.create_task(enqueue())

  async def worker(self) -> None:
    while True:
      task = await self.task_queue.get()
      try:
        await task()
      except Exception as e:
        print(e, flush=True)
        continue
