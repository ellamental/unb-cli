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


def _clean_config(d):
  return {k: v for k, v in d.items() if k.isupper() and not k.startswith('_')}


def _default_config_path():
  return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'default_config.py')


def _load_config(path=None, defaults=None):
  """Load the config at path, or the default config if path is not supplied."""
  if defaults is None:
    ret = _load_config(_default_config_path(), defaults={})
  else:
    ret = defaults
  if not path:
    # Return the default config only for projects without a config file.
    return Config(**_clean_config(ret))
  execfile(path, ret)
  return Config(**_clean_config(ret))


def _get_fuzzy_name(names, fuzzy_name):
  """Return the full project name that matches the fuzzy_name.

  Note: There may be multiple matches for fuzzy_name.  Currently this
  implementation will simply match the first occurance.  That is probably a
  bug, but until this is used more I'm not sure what it should do.

  Example:

      >>> names = ['my-project', 'unb-cli', 'unb-platform']
      # Project name starts with fuzzy_name
      >>> _get_fuzzy_name(names, 'm')
      'my-project'
      # Project name starts with fuzzy_name if "unb-" prefix is stripped
      >>> _get_fuzzy_name(names, 'plat')
      'unb-platform'
      # Multiple matches returns the first match
      # This behavior should not be relied upon!
      >>> _get_fuzzy_name(names, 'unb')
      'unb-cli'
  """
  for name in names:
    if (name.startswith(fuzzy_name) or
        name.lstrip('unb-').startswith(fuzzy_name)):  # noqa
      return name
  return None


class Project(object):
  """A unb-cli project and its configuration.

  Examples:

    # Get a project by its name.  The project name's "unb-" prefix, if
    # applicable, may be omitted.
    project = Project.get(name)

    # Get a project from a path.  The path may be the project's root, or any
    # subdirectory of the project root.
    project = Project.get(path)

    # Get the root path for the project.
    project.path

    # Get the (loaded) configuration instance for the project.
    project.config

    # Get the path to the project's config file.
    project.config_path

  """

  # TODO(nick): The anon stuff is a hack.  We should really set anon based on
  #   if we find a project from the given name/path, instead of doing it in the
  #   classmethods.
  def __init__(self, name=None, path=None, anon=False):
    if path and not name:
      name = os.path.split(path)[-1]
      self._path = path
    self.name = name
    self.anon = anon

  def __repr__(self):
    return 'Project(name="' + str(self.name) + '", path="' + self.path + '")'

  def build_config_path(self):
    if not self.name:
      return None
    return os.path.join(PROJECTS_PATH, self.name + '.py')

  @property
  def config_path(self):
    """Return the path to the config file for this project or None."""
    path = self.build_config_path()
    if os.path.exists(path):
      return path

  @property
  def config(self):
    if hasattr(self, '_config'):
      return self._config
    self._config = _load_config(self.config_path)
    return self._config

  @property
  def path(self):
    if hasattr(self, '_path'):
      return self._path
    self._path = self.config.get('PROJECT_PATH')
    return self._path

  @property
  def venv_path(self):
    """Get the full path to this project's virtual environment directory."""
    path = self.config.get('VENV_PATH')
    if path and os.path.exists(path):
      return path
    path = os.path.join(self.path, 'venv')
    if path and os.path.exists(path):
      return path
    if not self.name:
      return None
    default_venv_dir = os.path.join(os.path.expanduser('~'), '.virtualenvs')
    path = os.path.join(default_venv_dir, self.name)
    if os.path.exists(path):
      return path

  @property
  def venv_activate_path(self):
    """Get the full path to this project's venv/bin/activate script."""
    venv_path = self.venv_path
    if venv_path:
      return os.path.join(venv_path, 'bin', 'activate')

  def activate_venv(self):
    path = self.venv_path
    if path:
      activate_this = os.path.join(path, 'bin', 'activate_this.py')
      if os.path.exists(activate_this):
        execfile(activate_this, dict(__file__=activate_this))

  # Classmethods
  # ============

  @classmethod
  def list(cls):
    """List all projects with config files in ~/.unb-cli.d/projects/."""
    filenames = os.listdir(PROJECTS_PATH)
    return [f[:-3] for f in filenames if f.endswith('.py')]

  @classmethod
  def get(cls, name_or_path):
    if os.path.sep in name_or_path:
      return cls.get_from_path(name_or_path)
    return cls.get_from_name(name_or_path)

  @classmethod
  def get_from_name(cls, name):
    project_names = cls.list()
    name = _get_fuzzy_name(project_names, name)
    if name:
      return cls(name=name)

  @classmethod
  def get_from_path(cls, path):
    """Get an existing project or create and return an anonymous project.

    This method will *always* return a project.  If the path is not in an
    existing project, a temporary, anonymous project will be created and
    returned.
    """
    start_path = path
    while True:
      if os.path.exists(os.path.join(path, '.git')):
        return cls(path=path)
      if not path or path == ROOT_PATH:
        return cls(path=start_path, anon=True)
      path = os.path.dirname(path)


def copy_default_config(dest):
  """Copy the default config (useful for creating new projects)."""
  return shutil.copy(_default_config_path(), dest)


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
