import os
import subprocess

from lib.commands.commands import arg, Group

from . import config


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


@group.command(name='config-path')
@arg('name')
def config_path(name):
  """Get the full path to the project config file given a project name."""
  print project.config_path(name)


@group.command(name='config')
@arg('name')
def project_config(name):
  """Return the project configuration as a json object."""
  for key, value in project.config_dict(project.config_path(name)).items():
    print key, ':', value


@group.command(name='copy-default-config')
@arg('dest')
def copy_default_config(dest):
  """Copy the default project config to dest."""
  project.copy_default_config(dest)


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
  projects = project.list_projects()
  projects.sort()
  if projects:
    for project_name in projects:
      print project_name
  else:
    print 'No projects found.'


@group.command(name='current')
def project_current():
  """Get the project the current working directory is in."""
  project_path = project.find_parent_project_path(os.getcwd())
  if project_path:
    print project.get_project_name_from_path(project_path)


@group.command(name='path')
@arg('project_name', nargs='?', default=None)
def project_path(project_name):
  """Return the PROJECT_ROOT config value (optionally for a project_name)."""
  if project_name is None:
    project_path = config.PROJECT_PATH
  else:
    project_path = project.project_path(project_name)
  print project_path


@group.command(name='venv-activate-path')
@arg('project_name', nargs='?', default=None)
def project_venv_activate_path(project_name):
  """Return a path to the project's venv/bin/activate script."""
  if project_name is None:
    path = config.PROJECT_PATH
  else:
    path = project.project_path(project_name)
  activate_path = os.path.join(path, 'venv', 'bin', 'activate')
  print activate_path


@group.command()
def mkconfig():
  """Make the UNB CLI config directory structure."""
  project.make_config_dir()


@group.command()
def licenses():
  """List licenses of all 3rd party packages."""
  subprocess.call(['yolk', '-l', '-f', 'license'])


@group.command(name='config')
@arg('key', nargs='?')
def conf(key):
  """Access config settings (mostly a debugging tool)."""
  if not key:
    from unb_cli import random_tools
    random_tools.pp(config)
  else:
    key = key.upper()
    try:
      print "%s: %s" % (key, config[key])
    except KeyError:
      pass
