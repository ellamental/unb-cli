import os
import sys

from lib.commands.commands import Group

from unb_cli.config.utils import get_current_config


config = get_current_config()


def _is_django_project():
  """A, not totally reliable, test if we're in a Django project."""
  managepy_path = os.path.join(config.PROJECT_PATH, 'manage.py')
  if os.path.exists(managepy_path):
    return True
  return False


def cli_init():
  """Project management utilities."""
  project_path = config.get('PROJECT_PATH', config.HOME_PATH)

  if project_path != config.HOME_PATH:
    # Add the project path to sys.path for all utilities.
    sys.path.append(config.PROJECT_PATH)

  if _is_django_project():
    # Set the default settings module.
    os.environ.setdefault(
      'DJANGO_SETTINGS_MODULE',
      config.get('DEFAULT_DJANGO_SETTINGS_MODULE', 'settings'))



cli = Group(cli_init)
from . import main  # Adds directly to cli

# Each module under this exports ``group`` which is added here.
from . import project
cli.add_group(project.group, name='project')
