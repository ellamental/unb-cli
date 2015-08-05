"""
UNB CLI Default Configuration
=============================

Project paths and settings.


Config Inheritence
------------------

0) Default Config (here!)
1) Main Config (~/.unb-cli.d/config.py)
2) Main Projects (~/.unb-cli.d/projects/project-name.py)
3*) Project Config (project-path/.unb-cli || setup.cfg[unb-cli]?)

Each overwrites values from the previous.

"""

import os


UNB_CLI_D_DIRNAME = '.unb-cli.d'
PROJECTS_DIRNAME = 'projects'
CONFIG_FILENAME = 'config.py'

UNB_CLI_D_PATH = os.path.join(os.environ.get('HOME'), UNB_CLI_D_DIRNAME)
CONFIG_PATH = os.path.join(UNB_CLI_D, CONFIG_FILENAME)
PROJECTS_PATH = os.path.join(UNB_CLI_D, PROJECTS_DIRNAME)


def make_config_dir():
  """Create a config directory structure in the user's home directory."""
  if not os.path.exists(UNB_CLI_D_PATH):
    try:
      os.makedirs(UNB_CLI_D_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise

  if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'a+') as f:
      os.utime(CONFIG_PATH, None)  # roughly equivalent to: $ touch CONFIG_PATH

  if not os.path.exists(PROJECTS_PATH):
    try:
      os.makedirs(PROJECTS_PATH)
    except OSError:
      print "An error occured, please create directories manually."
      raise


def list_projects():
  project_filenames = os.listdir(PROJECTS_PATH)


def load_main_config():
  """
  This is where we'll list projects and stuff.

  Check for ~/.unb-cli
  Check for ~/.unb-cli.d/config.py
  """
  pass


def current_project():
  """
  1) Traverse up directories until a .git is found.
  2) Figure out how to associate that with a project/project_id.
  """
  pass


def load_project_config(project_id):
  """
  1) Load the project config from the main config.
  2) Load the project config overrides from the project dir.
  """


def project_config():
  """
  config = load_main_config()
  config.update(

  """


# TODO(nick): Convert configuration to project-based config.
# {
#   'project_name': {
#     'MANAGEMENT_DIR': 'example/whatevs',
#   },
# }



# Paths
# -----
# TODO(nick): These paths make a lot of assumptions about the project
#   configuration.  A more configurable option would be preferable.

# Management directories
MANAGEMENT_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.join(MANAGEMENT_DIR, 'scripts')
PROJECT_DIR = os.path.dirname(MANAGEMENT_DIR)

APP_DIR = os.path.join(PROJECT_DIR, 'unb')
DOCS_DIR = os.path.join(PROJECT_DIR, 'docs')
DOCS_BUILD_DIR = os.path.join(DOCS_DIR, '.build')
DOCS_MODULES_DIR = os.path.join(DOCS_DIR, 'modules')

VERSION_FILE = os.path.join(PROJECT_DIR, 'VERSION')

# pip requirements filenames/locations (relative to PROJECT_DIR)
REQUIREMENTS_FILE = 'requirements.txt'
DEV_REQUIREMENTS_FILE = 'dev-requirements.txt'


# Settings
# --------

# Set settings to dev, only if not already set in the environment.
DEFAULT_DJANGO_SETTINGS_MODULE = 'unb.settings.dev'
