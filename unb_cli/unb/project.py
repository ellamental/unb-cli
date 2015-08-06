import os

from lib.commands.commands import arg, Group

from unb_cli import project
from unb_cli.config.utils import get_project_path

from . import config


# Projects
# ========

group = Group(description='Project management utilities.')


def project_list():
  """List projects configured to use UNB CLI."""
  projects = project.list_all()
  projects.sort()
  if projects:
    print 'Projects(%s):' % len(projects)
    for project_name in projects:
      print '  - ', project_name
  else:
    print 'No projects found.'
group.command(project_list, name='list')


def project_current():
  """Get the project the current working directory is in."""
  project_name = project.get_project_name(project.current_project_path())
  if project_name:
    print project_name
  else:
    print 'Not in a project.'
group.command(project_current, name='current')


@arg('project_name', nargs='?', default=None)
def project_venv_activate_path(project_name):
  """Return a path to the project's venv/bin/activate script."""
  if project_name is None:
    path = config.PROJECT_PATH
  else:
    path = get_project_path(project_name)
  activate_path = os.path.join(path, 'venv', 'bin', 'activate')
  print activate_path
group.command(project_venv_activate_path, name='venv-activate-path')


@arg('project_name', nargs='?', default=None)
def project_path(project_name):
  """Return the PROJECT_ROOT config value (optionally for a project_name)."""
  if project_name is None:
    project_path = config.PROJECT_PATH
  else:
    project_path = get_project_path(project_name)
  print project_path
group.command(project_path, name='path')


def mkconfig():
  """Make the UNB CLI config directory structure."""
  project.make_config_dir()
group.command(mkconfig)
