import os
import subprocess

from clams import arg, Command

from unb_cli.project import Project, copy_default_config, make_config_dir
from . import current_project


project = Command(
  name='project',
  title='Project management utilities',
  description='''Project management utilities.

Tools that help you work with your projects, store and access configuration and
consolidate your tooling across projects.
''',
)


@project.register('new')
@arg('name')
def new(name):
  """Create a new project config at ~/.unb-cli.d/projects/{{name}}.py."""
  cp = Project.get(name)
  if cp:
    print 'Error: Project name already exists.  Path: ', cp.path
  config_path = cp.build_config_path()
  copy_default_config(config_path)


@project.register('list')
def project_list():
  """List projects configured to use UNB CLI."""
  projects = Project.list()
  if projects:
    projects.sort()
    for project_name in projects:
      print project_name
  else:
    print 'No projects found.'


@project.register('current')
def project_current():
  """Get the project the current working directory is in."""
  cp = current_project()
  if cp and not cp.anon:
    print cp.name


@project.register('path')
@arg('name', nargs='?', default=None)
def project_path(name):
  """Return the PROJECT_PATH (optionally for a project_name or (sub)path)."""
  if name is None:
    cp = current_project()
  else:
    cp = Project.get(name)
  if cp:
    print cp.path


@project.register('config-path')
@arg('name', nargs='?')
def config_path(name):
  """Get the full path to the project config file given a project name."""
  if not name:
    cp = current_project()
  else:
    cp = Project.get(name)
  if cp:
    print cp.config_path


@project.register('config')
@arg('name', nargs='?')
def project_config(name):
  """Print the project configuration as (key: value)."""
  if not name:
    cp = current_project()
  else:
    cp = Project.get(name)
  for key, value in cp.config.items():
    print key + ':', value


@project.register('conf')
@arg('key', nargs='?')
def conf(key):
  """Access config settings (mostly a debugging tool)."""
  cp = current_project()
  if not key:
    from unb_cli import random_tools
    random_tools.pp(cp.config)
  else:
    key = key.upper()
    try:
      print "%s: %s" % (key, cp.config[key])
    except KeyError:
      pass


@project.register('mkconfig')
def mkconfig():
  """Make the UNB CLI config directory structure."""
  make_config_dir()


@project.register('venv-activate-path')
@arg('project_name', nargs='?', default=None)
def project_venv_activate_path(project_name):
  """Return a path to the project's venv/bin/activate script."""
  if project_name is None:
    cp = current_project()
  else:
    cp = Project.get(project_name)
  venv_activate_path = cp.venv_activate_path
  if venv_activate_path:
    print venv_activate_path


@project.register('licenses')
def licenses():
  """List licenses of all 3rd party packages."""
  subprocess.call(['yolk', '-l', '-f', 'license'])


@project.register('bump')
@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version.bump_file(current_project().version_file_path, part, '0.0.0')


def _tag(version, message):
  """Create a git tag."""
  v = 'v' + version
  subprocess.call(['git', 'tag', '-a', v, '-m', message])


@project.register('tag')
@arg('message', nargs='?', default='')
def tag(message):
  """Create a git tag."""
  from unb_cli import version
  version_file_path = os.path.join(current_project().path,
                                   current_project().config.VERSION_FILENAME)
  v = version.read(version_file_path)
  _tag(v, message)


@project.register('version')
def get_version():
  """Get the version number of the current project."""
  from unb_cli import version
  v = version.read(current_project().version_file_path)
  if v is not None:
    print v
