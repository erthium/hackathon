import asyncio
import os
import subprocess
from http import HTTPStatus

from fastapi import HTTPException

# The location of the sandbox environment's compose.yaml
SANDBOX_COMPOSE_FILE_LOCATION = os.path.join(
  os.path.dirname(__file__), "../sandbox", "compose.yaml"
)


async def build_and_run_sandbox() -> asyncio.subprocess.Process:
  """Builds the sandbox environment using Docker Compose.

  Raises:
      HTTPException: If `docker compose build` fails, this error is thrown.

  Returns:
      asyncio.subprocess.Process: The `docker compose up` process along with its stdout and stderr.

      Note that the process is not awaited here, it should be awaited in the caller function.
  """

  # First, build the environment
  build_process = await asyncio.subprocess.create_subprocess_exec(
    "docker",
    "compose",
    "-f",
    SANDBOX_COMPOSE_FILE_LOCATION,
    "build",
    # "--no-cache", # TODO(brkdnmz): I assume this is not needed
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
  )

  # Using process.wait() alone may cause deadlock:
  # https://docs.python.org/3/library/asyncio-subprocess.html#:~:text=the%20returncode%20attribute.-,Note,-This%20method%20can
  stdout, stderr = await build_process.communicate()
  await build_process.wait()  # Wait until finished completely

  if build_process.returncode != 0:  # Build failed
    raise HTTPException(
      status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
      detail=f"An error occurred building the sandbox (exit code {build_process.returncode})",
    )

  # Build was succesful, run the sandbox
  compose_up_process = await asyncio.subprocess.create_subprocess_exec(
    "docker",
    "compose",
    "-f",
    SANDBOX_COMPOSE_FILE_LOCATION,
    "up",
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
  )

  # Return the process whether an error occurred or not
  return compose_up_process


# Currently unused
def stop_sandbox() -> subprocess.CompletedProcess[bytes]:
  docker_compose_process = subprocess.run(
    ["docker", "compose", "-f", SANDBOX_COMPOSE_FILE_LOCATION, "down"],
    capture_output=True,
  )
  return docker_compose_process
