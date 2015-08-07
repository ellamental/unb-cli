import os

from lib.commands.commands import arg, Group

from unb_cli import myprojects
from unb_cli.config.utils import get_project_path

from . import config


# Projects
# ========

group = Group(
  title='Project management utilities',
  description='''Project management utilities.

Tools that help you work with your projects, store and access configuration and
consolidate your tooling across projects.
''',
  epilog='''Here's more information that's really only here for example.

This epilog only shows up when you use the -h or --help options.  If you
display help by running a sub-group with too few arguments, you will never see
this!
''',
)


@group.command(name='list')
def project_list():
  """List projects configured to use UNB CLI."""
  projects = myprojects.list_all()
  projects.sort()
  if projects:
    print 'Projects(%s):' % len(projects)
    for project_name in projects:
      print '  - ', project_name
  else:
    print 'No projects found.'


@group.command(name='current')
def project_current():
  """Get the project the current working directory is in."""
  project_name = myprojects.get_project_name(myprojects.current_project_path())
  if project_name:
    print project_name
  else:
    print 'Not in a project.'


@group.command(name='venv-activate-path')
@arg('project_name', nargs='?', default=None)
def project_venv_activate_path(project_name):
  """Return a path to the project's venv/bin/activate script."""
  if project_name is None:
    path = config.PROJECT_PATH
  else:
    path = get_project_path(project_name)
  activate_path = os.path.join(path, 'venv', 'bin', 'activate')
  print activate_path


@group.command(name='path')
@arg('project_name', nargs='?', default=None)
def project_path(project_name):
  """Return the PROJECT_ROOT config value (optionally for a project_name)."""
  if project_name is None:
    project_path = config.PROJECT_PATH
  else:
    project_path = get_project_path(project_name)
  print project_path


@group.command()
def mkconfig():
  """Make the UNB CLI config directory structure."""
  myprojects.make_config_dir()
