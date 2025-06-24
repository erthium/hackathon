import os
import subprocess
from dotenv import load_dotenv

from template_checker import validate_template, get_command_exec


def main():
  load_dotenv()

  TEMPLATE_NAME = os.getenv("TEMPLATE_NAME")
  COMMAND_NAME = os.getenv("COMMAND_NAME")
  ARGS = os.getenv("ARGS")
  REPOSITORIES = ARGS.split(",")

  if not validate_template(TEMPLATE_NAME, verbose=True):
    print("Template validation failed.")
    exit(1)

  print("Template validation successful.")

  command_exec = get_command_exec(TEMPLATE_NAME, COMMAND_NAME, REPOSITORIES)

  # run the python command python3 command_exec *repositories
  # wait for the process to finish
  # print the output
  command_process = subprocess.run(["python3", command_exec, *REPOSITORIES], capture_output=True)
  print(command_process.stdout.decode())
  

if __name__ == "__main__":
  main()
