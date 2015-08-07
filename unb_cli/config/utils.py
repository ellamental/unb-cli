"""
UNB CLI Configuration Utilities

This module presents utilities for locating, loading and accessing
UNB CLI project configuration files.


Config Inheritence
------------------

0) Defaults (config.defaults.merge_overrides)
1*) Main Config (~/.unb-cli.d/config.py)
2) Main Projects (~/.unb-cli.d/projects/project-name.py)
3*) Project Config (project-path/.unb-cli || setup.cfg[unb-cli]?)

* Not implemented

Each overwrites values from the previous.

"""

import os
import sys

from . import cli as config_cli
from . import defaults

from unb_cli import myprojects


class Config(dict):
  """Simple dict wrapper that allows dotted lookup (e.g., config.attr).

  Raises:

    AttributeError: When attribute does not exist for both attribute lookup
      (config.attr) and item lookup (config['attr']).
  """

  def __init__(self, **kwargs):
    super(Config, self).__init__(**kwargs)

  def __getattr__(self, name):
    """Delegate attribute lookup to __getitem__."""
    return self.__getitem__(name)

  def __getitem__(self, name):
    return super(Config, self).__getitem__(name)


# Find Config Modules
# ===================

def find_config_modules(project_name):
  """Check standard locations for config modules and return them if present."""
  # TODO(nick): Finish me!
  myprojects.get_path(project_name)


# Import Modules
# ==============

def get_default_config_module():
  config_module = __import__(config_cli.DEFAULT_CONFIG_DOTTED_PATH)
  defaults_module = getattr(config_module,
                            config_cli.DEFAULT_CONFIG_MODULE_NAME)
  return defaults_module


def get_config_module(project_name):
  if not project_name:
    return {}
  project_filename = project_name + '.py'
  config_path = os.path.join(config_cli.PROJECTS_PATH, project_filename)
  if os.path.exists(config_path):
    dotted_name = '.'.join([config_cli.PROJECTS_DIRNAME, project_name])

    # Add the config directory to the system path so we can import the config.
    # Then remove it so we don't go clobbering imports elsewhere.
    # TODO(nick): There's got to be a better way to do this!
    if config_cli.UNB_CLI_D_PATH not in sys.path:
      sys.path.append(config_cli.UNB_CLI_D_PATH)
    packages_module = __import__(dotted_name)
    sys.path.remove(config_cli.UNB_CLI_D_PATH)

    project_module = getattr(packages_module, project_name)
    return project_module
  else:
    return {}


# Get Config Attributes
# =====================

def convert_module_to_config_dict(config_module):
  ret = {}
  for attr in dir(config_module):
    is_public_config = not attr.startswith('_') and attr.isupper()
    if is_public_config:
      ret[attr] = getattr(config_module, attr)
  return ret


def get_config_values(config_module):
  overrides_dict = convert_module_to_config_dict(config_module)
  config_dict = defaults.merge_overrides(overrides_dict)
  c = Config(**config_dict)
  return c


# High-Level API
# ==============

def get_config(project_name):
  config_module = get_config_module(project_name)
  config_values = get_config_values(config_module)
  return config_values


def get_current_config():
  project_name = myprojects.get_project_name(myprojects.current_project_path())
  return get_config(project_name)


def get_project_path(project_name):
  proj_conf = get_config(project_name)
  return proj_conf.get('PROJECT_PATH')
