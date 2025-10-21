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
import yaml
from typing import List, Optional, Union
from functools import lru_cache

from app.logger import logger
from app.core.settings import app_settings
from app.objects.template import ScoreMetric, Command, Template
from app.objects.enums import CommandArgType


# Constant config values
CONFIG_FILENAME: str = "config.yaml" 
GENERIC_CONFIG_KEYS: dict = {
  "name": str,
  "description": str,
  "version": str,
  "author": str,
  "user_template_dir": str,
  "on_submission_command": str,
  "on_competition_end_command": Optional[str],
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
SCORES_KEY: str = "score_metrics"
REQUIRED_SCORE_KEYS: dict = {
  "description": str,
  "is_ascending": bool,
  "min_value": Union[int, float, None],
  "max_value": Union[int, float, None],
  "is_primary": bool,
  "is_public": bool,
}


class TemplateService:
  def __init__(self):
    pass


  def _validate_template(self, template_dir: str) -> bool:
    # Check if the template directory has a config.yaml file
    config_file_path: str = os.path.join(template_dir, CONFIG_FILENAME)
    if not os.path.exists(config_file_path):
      logger.info(f"Missing {CONFIG_FILENAME}\n")
      return False
    
    # Check if the config.yaml file is in the correct format
    try:
      with open(config_file_path, "r") as f:
        config: dict = yaml.safe_load(f)

        # Check if the config has the correct keys and values
        for key, value in GENERIC_CONFIG_KEYS.items():
          if key not in config:
            logger.info(f"Missing key: {key}")
            return False

          if not isinstance(config[key], value):
            logger.info(f"Expected {key} to be of type {value.__name__}, got {type(config[key]).__name__}")
            return False

        # Check if the commands are in the correct format
        if COMMANDS_KEY not in config:
          return False
        else:
          for command_name, command in config[COMMANDS_KEY].items():
            for key, value in REQUIRED_COMMAND_KEYS.items():
              if key not in command:
                logger.info(f"Missing key: {key} in command: {command_name}")
                return False

              if not isinstance(command[key], value):
                logger.info(f"Expected {key} to be of type {value.__name__}, got {type(command[key]).__name__}")
                return False

        # Check if the scores are in the correct format
        if SCORES_KEY not in config:
          logger.info(f"Missing key: {SCORES_KEY}")
          return False
        else:
          for score_name, score in config[SCORES_KEY].items():
            for key, value in REQUIRED_SCORE_KEYS.items():
              if key not in score:
                logger.info(f"Missing key: {key} in score: {score_name}")
                return False
              # Accept tuple for min_value/max_value (int or None)
              if isinstance(value, tuple):
                if not isinstance(score[key], value):
                  logger.info(f"Expected {key} to be of type {value}, got {type(score[key]).__name__}")
                  return False
              else:
                if not isinstance(score[key], value):
                  logger.info(f"Expected {key} to be of type {value.__name__}, got {type(score[key]).__name__}")
                  return False

    except yaml.YAMLError as yaml_error:
      logger.info(f"Error decoding YAML file: {yaml_error}")
      return False

    except Exception as exception:
      logger.info(f"An error occurred: {exception}")
      return False

    return True


  def _get_template(self, template_dir: str) -> Template:
    with open(os.path.join(template_dir, CONFIG_FILENAME), "r") as f:
      config: dict = yaml.safe_load(f)
      score_metrics: List[ScoreMetric] = []
      for score_name, score in config[SCORES_KEY].items():
        score_metrics.append(
          ScoreMetric(
            name=score_name,
            description=score["description"],
            is_ascending=score["is_ascending"],
            is_primary=score["is_primary"],
            is_public=score["is_public"],
            min_value=score.get("min_value", None),
            max_value=score.get("max_value", None)
          )
        )

      commands: List[Command] = []
      for command_name, command in config[COMMANDS_KEY].items():
        commands.append(
          Command(
            name=command_name,
            description=command["description"],
            usage=command.get("usage", ""),
            execute=command["execute"],
            arg_type=CommandArgType(command["arg_type"]),
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
        commands=commands,
        on_submission_command=config.get("on_submission_command", None),
        on_competition_end_command=config.get("on_competition_end_command", None),
        score_metrics=score_metrics
      )


  def get_all_templates(self) -> List[Template]:
    templates: List[Template] = []
    TEMPLATES_DIR = app_settings.TEMPLATES_DIR
    if not os.path.exists(TEMPLATES_DIR):
      raise FileNotFoundError(f"Template directory {TEMPLATES_DIR} does not exist")
    if not os.path.isdir(TEMPLATES_DIR):
      raise NotADirectoryError(f"Template directory {TEMPLATES_DIR} is not a directory")
    for template_dir_name in os.listdir(TEMPLATES_DIR):
      template_dir = os.path.join(TEMPLATES_DIR, template_dir_name)
      if not os.path.isdir(template_dir):
        continue
      
      if self._validate_template(template_dir):
        templates.append(self._get_template(template_dir))

    return templates


  def get_template_by_name(self, name: str) -> Template:
    TEMPLATES_DIR = app_settings.TEMPLATES_DIR
    template_dir = os.path.join(TEMPLATES_DIR, name)
    if not os.path.exists(template_dir):
      raise FileNotFoundError(f"Template {name} not found")

    if not self._validate_template(template_dir):
      raise ValueError(f"Template {name} is not in the correct format")

    return self._get_template(template_dir)


@lru_cache
def get_template_service() -> TemplateService:
  return TemplateService()
