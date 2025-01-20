import os
import sys
import importlib.util
from typing import Type


def import_module(module_dir: str, module_name: str) -> importlib.util.types.ModuleType:
  """
  Import a module from a given directory.
  :param module_dir: The directory where the module is located.
  :param module_name: The name of the module to import.
  :return: The imported module.
  """
  # Validate the given path
  if not os.path.isdir(module_dir):
    raise FileNotFoundError(f"The directory {module_dir} does not exist.")

  # Construct the path to the module
  module_path = os.path.join(module_dir, module_name)
  if not os.path.isfile(module_path):
    raise FileNotFoundError(f"Module not found in {module_path}.")

  spec = importlib.util.spec_from_file_location(module_name, module_path)
  imported_module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = imported_module
  spec.loader.exec_module(imported_module)

  return imported_module


def import_attribute(module_dir: str, module_name: str, import_attr: str) -> Type:
  """
  Import a module from a given directory and return a specific attribute from it.
  Uses 'import_module' to import the module.
  Raises AttributeError if the attribute is not found.
  :param module_dir: The directory where the module is located.
  :param module_name: The name of the module to import.
  :param import_attr: The attribute to import from the module.
  :return: The imported attribute.
  """
  imported_module = import_module(module_dir, module_name)

  if not hasattr(imported_module, import_attr):
    raise AttributeError(f"Attribute {import_attr} not found in module {module_name} in directory {module_dir}.")

  return imported_module.__getattribute__(import_attr)
