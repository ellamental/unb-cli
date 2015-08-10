"""Creating and managing unb-cli projects."""

import os

from unb_cli.config import cli as config_cli


def list_all():
  filenames = os.listdir(config_cli.PROJECTS_PATH)
  return [f[:-3] for f in filenames
          if f.endswith('.py') and not f.startswith('__')]


def current_project_path():
  """Retrieve the base path of the project containing the cwd.

  Note: This may not be a valid unb-cli project!  It will return the base path
    of any git project.
  """
  import os
  current_dir = os.getcwd()
  while True:
    if os.path.exists(os.path.join(current_dir, '.git')):
      return current_dir
    if not current_dir or current_dir == config_cli.ROOT_PATH:
      return None
    current_dir = os.path.dirname(current_dir)


def get_project_name(project_path):
  """Retrieve a project name given a project_path.

  Note: Currently projects must be named the same as their directory names and
    duplicate project names are not allowed.

  TODO(nick): Allow the project name to differ from the project directory name.
  """
  if project_path:
    return os.path.split(project_path)[-1]
  return ''


# UNB-CLI Configuration Initialization
# ====================================

def make_config_dir():
  """Create a standard config directory structure in the user's home directory.

  The directory structure should be:

      $HOME/
          .unb-cli.d/
              config.py
              projects/
                  project-name.py
                  ...
  """
  if not os.path.exists(config_cli.UNB_CLI_D_PATH):
    try:
      os.makedirs(config_cli.UNB_CLI_D_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise

  if not os.path.exists(config_cli.CONFIG_PATH):
    with open(config_cli.CONFIG_PATH, 'a+') as f:
      f.write('')
      # could also do:
      # os.utime(CONFIG_PATH, None)  # roughly equivalent to: touch CONFIG_PATH

  if not os.path.exists(config_cli.PROJECTS_PATH):
    try:
      os.makedirs(config_cli.PROJECTS_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise
