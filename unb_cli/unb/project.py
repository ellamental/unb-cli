import os
import subprocess

from lib.commands.commands import arg, Group

from . import current_project


# Projects
# ========

group = Group(
  title='Project management utilities',
  description='''Project management utilities.

Tools that help you work with your projects, store and access configuration and
consolidate your tooling across projects.
''',
)


from unb_cli import project
from unb_cli.project import Project


@group.command(name='new')
@arg('name')
def new(name):
  """Create a new project config at ~/.unb-cli.d/projects/{{name}}.py."""
  existing_config_path = project.config_path(name)
  if existing_config_path:
    print 'Error: Project name already exists.  Path: ', existing_config_path
  config_path = project.make_config_path(name)
  project.copy_default_config(config_path)


@group.command(name='list')
def project_list():
  """List projects configured to use UNB CLI."""
  projects = Project.list()
  if projects:
    projects.sort()
    for project_name in projects:
      print project_name
  else:
    print 'No projects found.'


@group.command(name='current')
def project_current():
  """Get the project the current working directory is in."""
  project = current_project()
  if project:
    print project.name


@group.command(name='path')
@arg('name', nargs='?', default=None)
def project_path(name):
  """Return the PROJECT_PATH (optionally for a project_name or (sub)path)."""
  if name is None:
    project = current_project()
  else:
    project = Project.get(name)
  if project:
    print project.path


@group.command(name='config-path')
@arg('name')
def config_path(name):
  """Get the full path to the project config file given a project name."""
  project = Project.get(name)
  if project:
    print project.config_path


@group.command(name='config')
@arg('name', nargs='?')
def project_config(name):
  """Print the project configuration as (key: value)."""
  if not name:
    project = current_project()
  else:
    project = Project.get(name)
  for key, value in project.config.items():
    print key + ':', value


@group.command(name='copy-default-config')
@arg('dest')
def copy_default_config(dest):
  """Copy the default project config to dest."""
  project.copy_default_config(dest)


@group.command(name='conf')
@arg('key', nargs='?')
def conf(key):
  """Access config settings (mostly a debugging tool)."""
  project = current_project()
  if not key:
    from unb_cli import random_tools
    random_tools.pp(project.config)
  else:
    key = key.upper()
    try:
      print "%s: %s" % (key, project.config[key])
    except KeyError:
      pass


@group.command()
def mkconfig():
  """Make the UNB CLI config directory structure."""
  project.make_config_dir()


@group.command(name='venv-activate-path')
@arg('project_name', nargs='?', default=None)
def project_venv_activate_path(project_name):
  """Return a path to the project's venv/bin/activate script."""
  if project_name is None:
    p = current_project()
  else:
    p = Project.get(project_name)
  activate_path = project.venv_activate_path(p.path)
  if activate_path:
    print activate_path


@group.command()
def licenses():
  """List licenses of all 3rd party packages."""
  subprocess.call(['yolk', '-l', '-f', 'license'])


@group.command()
@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version_file_path = os.path.join(current_project().path,
                                   current_project().config.VERSION_FILENAME)
  version.bump_file(version_file_path, part, '0.0.0')


def _tag(version, message):
  """Create a git tag."""
  v = 'v' + version
  subprocess.call(['git', 'tag', '-a', v, '-m', message])


@group.command()
@arg('message', nargs='?', default='')
def tag(message):
  """Create a git tag."""
  from unb_cli import version
  version_file_path = os.path.join(current_project().path,
                                   current_project().config.VERSION_FILENAME)
  v = version.read(version_file_path)
  _tag(v, message)
