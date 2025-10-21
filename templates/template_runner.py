import os
import sys
import argparse
import subprocess

from template_checker import validate_template, get_command_exec


def main():
  parser = argparse.ArgumentParser(description="Run a command on a template with specified repositories.")
  parser.add_argument("--template-name", type=str, required=True, help="Name of the template.")
  parser.add_argument("--command-name", type=str, required=True, help="Name of the command to run.")
  parser.add_argument("--args", type=str, required=True, help="Comma-separated list of repository paths.")

  args = parser.parse_args()
  TEMPLATE_NAME = args.template_name
  COMMAND_NAME = args.command_name
  ARGS = args.args

  ALL_ARGS = ARGS.split(",")

  # TODO: Since the validation process happens during the template registration, we do not have to validate the template again in here
  if not validate_template(TEMPLATE_NAME, verbose=True):
    print("Template validation failed.")
    exit(1)

  print("Template validation successful.")

  REQUIREMENTS_PATH = os.path.join(TEMPLATE_NAME, "requirements.txt")
  if os.path.exists(REQUIREMENTS_PATH):
    print(f"Installing requirements from {REQUIREMENTS_PATH}...")
    subprocess.run(["pip", "install", "-r", REQUIREMENTS_PATH], check=True)
  else:
    print(f"No requirements.txt found in {TEMPLATE_NAME}, skipping installation.")
    return

  command_exec = get_command_exec(TEMPLATE_NAME, COMMAND_NAME, ALL_ARGS)
  print(f"Command to execute: {command_exec}")

  # run the python command python3 command_exec *repositories
  # wait for the process to finish
  # print the output
  command_process = subprocess.run(
    ["python3", command_exec, *ALL_ARGS],
    capture_output=True,
    cwd=TEMPLATE_NAME,
  )

  print("Output:")
  print(command_process.stdout.decode())
  if command_process.returncode != 0:
    print(f"Command failed with return code {command_process.returncode}")
    print("Error output:")
    print(command_process.stderr.decode())


if __name__ == "__main__":
  main()
