import os
import shutil


UNB_CLI_D_DIRNAME = '.unb-cli.d'
PROJECTS_DIRNAME = 'projects'
TEMPLATES_DIRNAME = 'templates'
CONFIG_FILENAME = '__config__.py'

ROOT_PATH = os.path.abspath(os.sep)
HOME_PATH = os.environ.get('HOME')
UNB_CLI_D_PATH = os.path.join(HOME_PATH, UNB_CLI_D_DIRNAME)
PROJECTS_PATH = os.path.join(UNB_CLI_D_PATH, PROJECTS_DIRNAME)
TEMPLATES_PATH = os.path.join(UNB_CLI_D_PATH, TEMPLATES_DIRNAME)


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


# Project Configuration Loading and Copying
# =========================================

def _clean_config(d):
  return {k: v for k, v in d.items() if k.isupper() and not k.startswith('_')}


def _default_config_path():
  return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'default_config.py')

def _default_config():
  return _load_config(_default_config_path(), defaults={})


def _load_config(path, defaults=None):
  if defaults is None:
    ret = _default_config()
  else:
    ret = defaults
  if not path:
    return Config(**_clean_config(ret))
  execfile(path, ret)
  return Config(**_clean_config(ret))


def make_config_path(project_name):
  if not project_name.endswith('.py'):
    project_name = project_name + '.py'
  return os.path.join(PROJECTS_PATH, project_name)


def config_path(project_name):
  """Get the full path to the project config file given a project name."""
  projects_path = PROJECTS_PATH
  project_names = os.listdir(projects_path)
  for name in project_names:
    stripped = name.rstrip('.py')
    if project_name == stripped or project_name == stripped.lstrip('unb-'):
      return os.path.join(projects_path, name)


def config(config_path):
  """Return the project configuration as a Config object."""
  return _load_config(config_path)


def copy_default_config(dest):
  """Copy the default config (useful for creating new projects)."""
  return shutil.copy(_default_config_path(), dest)


# Project Management Functions
# ============================

def new(name):
  pass


def list_projects():
  filenames = os.listdir(PROJECTS_PATH)
  return [f[:-3] for f in filenames
          if f.endswith('.py') and not f.startswith('__')]


def project_path(project_name_or_path):
  if os.path.exists(project_name_or_path):
    return find_parent_project_path(project_name_or_path)
  else:
    path = config_path(project_name_or_path)
    if path:
      return config(path).get('PROJECT_PATH')


def find_parent_project_path(path):
  """If path is in a project, return the project path, otherwise return None.

  Note: This may not be a valid unb-cli project!  It will return the base path
    of any git project.
  """
  while True:
    if os.path.exists(os.path.join(path, '.git')):
      return path
    if not path or path == ROOT_PATH:
      return None
    path = os.path.dirname(path)


def get_project_name_from_path(project_path):
  """Retrieve a project name given a project_path.

  Note: Currently projects must be named the same as their directory names and
    duplicate project names are not allowed.

  TODO(nick): Allow the project name to differ from the project directory name.
  """
  if project_path:
    return os.path.split(project_path)[-1]
  return ''


def venv_path(project_path):
  """Given a project path, return the path to the venv for that project."""
  if project_path:
    return os.path.join(project_path, 'venv')


def venv_activate_path(project_path):
  """Given a project path, return the path to the activate script."""
  project_venv_path = venv_path(project_path)
  if project_venv_path:
    activate_path = os.path.join(project_venv_path, 'bin', 'activate')
    if os.path.exists(activate_path):
      return activate_path


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
              templates/
                  template-name/
                      __config__.py
                      ...
                  ...

  Raises:
    OSError: If path is created between call to os.path.exists and os.makedirs.
  """
  if not os.path.exists(UNB_CLI_D_PATH):
    os.makedirs(UNB_CLI_D_PATH)

  if not os.path.exists(PROJECTS_PATH):
    os.makedirs(PROJECTS_PATH)

  if not os.path.exists(TEMPLATES_PATH):
    os.makedirs(TEMPLATES_PATH)
