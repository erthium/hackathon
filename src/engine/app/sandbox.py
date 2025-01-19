import os
import subprocess
from http import HTTPStatus

from fastapi import HTTPException

SANDBOX_COMPOSE_FILE_LOCATION = os.path.join(
  os.path.dirname(__file__), "../sandbox", "compose.yaml"
)


def build_and_run_sandbox() -> subprocess.CompletedProcess[bytes]:
  """Builds the sandbox environment using Docker Compose.

  Raises:
      HTTPException: If compose build fails, this error is thrown.

  Returns:
      subprocess.CompletedProcess[bytes]: The compose up process along with useful information (stdout, stderr etc.).
  """

  # The location of the sandbox environment's compose.yaml

  # First, build the environment with the `--no-cache` flag to ensure building from scratch.
  build_process = subprocess.run(
    [
      "docker",
      "compose",
      "-f",
      SANDBOX_COMPOSE_FILE_LOCATION,
      "build",
      "--no-cache",
    ],
    capture_output=True,
  )

  if build_process.returncode != 0:  # Build failed
    raise HTTPException(
      status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
      detail="An error occurred building the sandbox",
    )

  # Build was succesful, run the sandbox
  compose_up_process = subprocess.run(
    [
      "docker",
      "compose",
      "-f",
      SANDBOX_COMPOSE_FILE_LOCATION,
      "up",
    ],
    capture_output=True,
  )

  return compose_up_process


# Currently unused
def stop_sandbox() -> subprocess.CompletedProcess[bytes]:
  docker_compose_process = subprocess.run(
    ["docker", "compose", "-f", SANDBOX_COMPOSE_FILE_LOCATION, "down"],
    capture_output=True,
  )
  return docker_compose_process
