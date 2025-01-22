import json

from app.objects.engine import EngineTestFailedResult, EngineTestResult
from app.sandbox import build_and_run_sandbox
from pydantic import TypeAdapter, ValidationError


async def fake_test() -> EngineTestResult:
  """Runs a fake test without cloning a repository.

  Returns:
    EngineTestResult: The result of the test.
  """
  docker_compose_up_process = await build_and_run_sandbox()

  stdout, stderr = await docker_compose_up_process.communicate()

  if docker_compose_up_process.returncode != 0:
    return EngineTestFailedResult(error=stderr.decode())

  with open("sandbox/results/result.json", "r") as results_file:
    ta: TypeAdapter[EngineTestResult] = TypeAdapter(EngineTestResult)
    try:
      result = json.load(results_file)
      validated_result = ta.validate_python(result)
      return validated_result
    except ValidationError as e:
      # TODO: Should probably do smt else since it's not actually competitor's mistake but the template's
      return EngineTestFailedResult(
        error=f"Error occurred validating the engine template's result: {e}"
      )
