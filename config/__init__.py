"""
UNB CLI Default Configuration
=============================

Project paths and settings.


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

import cli_config as cfg
import defaults
import project


sys.path.append(cfg.UNB_CLI_D_PATH)


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


# Import Modules
# ==============

def get_default_config_module():
  config_module = __import__(cfg.DEFAULT_CONFIG_DOTTED_PATH)
  defaults_module = getattr(config_module, cfg.DEFAULT_CONFIG_MODULE_NAME)
  return defaults_module


def get_config_module(project_name):
  project_filename = project_name + '.py'
  config_path = os.path.join(cfg.PROJECTS_PATH, project_filename)
  if os.path.exists(config_path):
    dotted_name = '.'.join([cfg.PROJECTS_DIRNAME, project_name])
    packages_module = __import__(dotted_name)
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
  project_name = project.get_project_name(project.current_project_path())
  return get_config(project_name)


config = get_current_config()
