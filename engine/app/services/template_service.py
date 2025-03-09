"""
This service is used to obtain templates and their configurations.
"""
"""Example template config.json file:
{
  "name": "rpg",
  "description": "A template for RPG games",
  "version": "0.0.1",
  "author": "itu-ai",
  "user_template_dir": "user_template",
  "commands": {
    "test": {
      "description": "Checking if the submission works correctly",
      "usage": "test <path-to-repo>",
      "execute": "test.py",
      "args": ["--sender-repo"],
      "allocated_ram": 1024,
      "allocated_v_ram": 1024,
      "allocated_cpu": 1,
      "timeout": 60
    },
    "evaluate": {
      "description": "Finalising the competition and evaluating the submissions according to the rules",
      "usage": "evaluate +<path-to-repo>",
      "execute": "evaluate.py",
      "args": ["--all-repos"],
      "allocated_ram": 1024,
      "allocated_v_ram": 1024,
      "allocated_cpu": 1,
      "timeout": 60
    }
  }
}
"""

import os
import json
from typing import List
from functools import lru_cache

from app.core.settings import app_settings
from app.objects.template import Command, Template


# Constant config values
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


class TemplateService:
  def __init__(self):
    pass


  def _validate_template(self, template_dir: str) -> bool:
    # Check if the template directory has a config.json file
    config_file_path: str = os.path.join(template_dir, CONFIG_FILENAME)
    if not os.path.exists(config_file_path):
      print(f"Missing {CONFIG_FILENAME}\n")
      return False
    
    # Check if the config.json file is in the correct format
    try:
      with open(config_file_path, "r") as f:
        config: dict = json.load(f)

        # Check if the config has the correct keys and values
        for key, value in GENERIC_CONFIG_KEYS.items():
          if key not in config:
            print(f"Missing key: {key}")
            return False

          if not isinstance(config[key], value):
            print(f"Expected {key} to be of type {value.__name__}, got {type(config[key]).__name__}")
            return False

        # Check if the commands are in the correct format
        if COMMANDS_KEY not in config:
          return False
        else:
          for command_name, command in config[COMMANDS_KEY].items():
            for key, value in REQUIRED_COMMAND_KEYS.items():
              if key not in command:
                print(f"Missing key: {key} in command: {command_name}")
                return False

              if not isinstance(command[key], value):
                print(f"Expected {key} to be of type {value.__name__}, got {type(command[key]).__name__}")
                return False

    except json.JSONDecodeError:
      print(f"Error decoding JSON file")
      return False

    except Exception as exception:
      print(f"An error occurred: {exception}")
      return False
    
    return True


  def _get_template(self, template_dir: str) -> Template:
    with open(os.path.join(template_dir, CONFIG_FILENAME), "r") as f:
      config: dict = json.load(f)
      commands: List[Command] = []
      for command_name, command in config[COMMANDS_KEY].items():
        commands.append(
          Command(
            name=command_name,
            description=command["description"],
            usage=command.get("usage", ""),
            execute=command["execute"],
            arg_type=command["arg_type"],
            allocated_ram=command["allocated_ram"],
            allocated_v_ram=command["allocated_v_ram"],
            allocated_cpu=command["allocated_cpu"],
            timeout=command.get("timeout", None)
          )
        )

      return Template(
        name=config["name"],
        description=config["description"],
        version=config["version"],
        author=config["author"],
        user_template_dir=config["user_template_dir"],
        commands=commands
      )


  def get_all_templates(self) -> List[Template]:
    templates: List[Template] = []
    TEMPLATE_DIR = app_settings.TEMPLATE_DIR
    print(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
    for template_dir_name in os.listdir(TEMPLATE_DIR):
      template_dir = os.path.join(TEMPLATE_DIR, template_dir_name)
      print(f"template_dir: {template_dir}")
      if not os.path.isdir(template_dir):
        continue
      print(f"found dir {template_dir}")
      
      if self._validate_template(template_dir):
        templates.append(self._get_template(template_dir))
        print(f"appended template {template_dir}")
    return templates


  def get_template_by_name(self, name: str) -> Template:
    TEMPLATE_DIR = app_settings.TEMPLATE_DIR
    template_dir = os.path.join(TEMPLATE_DIR, name)
    if not os.path.exists(template_dir):
      raise FileNotFoundError(f"Template {name} not found")

    if not self._validate_template(template_dir):
      raise ValueError(f"Template {name} is not in the correct format")

    return self._get_template(template_dir)


@lru_cache
def get_template_service() -> TemplateService:
  return TemplateService()
