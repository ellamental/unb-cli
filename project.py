"""Creating and managing unb-cli projects."""

import os

import cli_config as cfg


def make_config_dir():
  """Create a config directory structure in the user's home directory."""
  if not os.path.exists(cfg.UNB_CLI_D_PATH):
    try:
      os.makedirs(cfg.UNB_CLI_D_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise

  if not os.path.exists(cfg.CONFIG_PATH):
    with open(cfg.CONFIG_PATH, 'a+') as f:
      f.write('')
      # could also do:
      # os.utime(CONFIG_PATH, None)  # roughly equivalent to: touch CONFIG_PATH

  if not os.path.exists(cfg.PROJECTS_PATH):
    try:
      os.makedirs(cfg.PROJECTS_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise


def list_projects():
  filenames = os.listdir(cfg.PROJECTS_PATH)
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
    if not current_dir or current_dir == cfg.ROOT_PATH:
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
