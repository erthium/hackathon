"""
This is a standalone script to see the current templates and if they obey the rules.
Mostly will be used to check if the config.json is in the correct format and has correct/existing values.
"""

import os
import json
from typing import List


# Constants
## Paths
SCRIPT_FILE: str = os.path.abspath(__file__)
TEMPLATE_DIRECTORY: str = os.path.dirname(SCRIPT_FILE)

## Config keys and values
CONFIG_FILENAME: str = "config.json" 
GENERIC_CONFIG_KEYS: dict = {
  "name": str,
  "description": str,
  "version": str,
  "author": str,
  "user_template_dir": str
}
COMMANDS_KEY: str = "commands"
REQUIRED_COMMAND_KEYS: dict = {
  "description": str,
  "execute": str,
  "arg_type": str,
  "allocated_ram": int,
  "allocated_v_ram": int,
  "allocated_cpu": int
}


def validate_template(template_dir: str, verbose: bool = False) -> bool:
  messages: list = []

  if verbose:
    print("-" * 50)
    print(f"Template: {os.path.basename(template_dir)}")

  # Check if the template directory has a config.json file
  config_file_path: str = os.path.join(template_dir, CONFIG_FILENAME)
  if not os.path.exists(config_file_path):
    if verbose:
      print(f"Missing {CONFIG_FILENAME}\n")
    return False
  
  # Check if the config.json file is in the correct format
  try:
    with open(config_file_path, "r") as f:
      config: dict = json.load(f)

      # Check if the config has the correct keys and values
      for key, value in GENERIC_CONFIG_KEYS.items():
        if key not in config:
          messages.append(f"Missing key: {key}")
          continue
        if not isinstance(config[key], value):
          messages.append(f"Expected {key} to be of type {value.__name__}, got {type(config[key]).__name__}")

      # Check if the commands are in the correct format
      if COMMANDS_KEY not in config:
        messages.append(f"Missing key: {COMMANDS_KEY}")
      else:
        for command_name, command in config[COMMANDS_KEY].items():
          for key, value in REQUIRED_COMMAND_KEYS.items():
            if key not in command:
              messages.append(f"Missing key: {key} in command: {command_name}")
              continue
            if not isinstance(command[key], value):
              messages.append(f"Expected {key} to be of type {value.__name__}, got {type(command[key]).__name__}")

  except json.JSONDecodeError:
    messages.append(f"Invalid JSON format in {CONFIG_FILENAME}")

  except Exception as exception:
    messages.append(f"Unhandled error: {exception}")

  if verbose:
    print("\n".join(messages), end="\n")
  
  return not messages


def get_command_exec(template_dir: str, command_name: str, args: List[str] = []) -> str:
  # get command list from config.json
  config_file_path: str = os.path.join(template_dir, CONFIG_FILENAME)
  with open(config_file_path, "r") as f:
    config: dict = json.load(f)
    commands = config.get(COMMANDS_KEY, {})
    command = commands.get(command_name, None)
    assert command, f"Command {command_name} not found in {config_file_path}"
    
    # check if the required args are provided
    required_args = command.get("args", "")
    if required_args == "--sender-repo":
      assert len(args) == 1, f"Expected 1 argument, got {len(args)}"
    elif required_args == "--all-repos":
      assert len(args) > 1, f"Expected more than 1 argument, got {len(args)}"
    
    return command["execute"]


def main() -> None:
  import argparse
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("-v", "--verbose", action="store_true", help="prints more information")
  args = parser.parse_args()
  verbose = args.verbose

  templates: dict = {}
  for template_dir_name in os.listdir(TEMPLATE_DIRECTORY):
    template_dir = os.path.join(TEMPLATE_DIRECTORY, template_dir_name)
    if not os.path.isdir(template_dir):
      continue

    templates[template_dir_name] = validate_template(template_dir, verbose)
  
  valid_template_count = sum(templates.values())
  total_template_count = len(templates)

  print(f"\nNumber of directories checked: {total_template_count}", f"Number of valid templates: {valid_template_count}", sep="\n", end="\n\n")


if __name__ == "__main__":
  main()
