"""
unb
===

Overview
--------

A shell utility (``unb``) is provided to accomplish common development tasks
with the UNB project.


Installation
------------

The ``unb`` utility is meant to be installed into and run in a virtual
environment.

The following install instructions assume you have already installed the shell
utility ``unb-go``, also found in this package.

::

   unb-go
   cd management/
   pip install --editable .

After installing, the ``unb`` command will be available.


Documentation and Usage
-----------------------

The unb utility's documentation is available through the ``--help`` option.

::

   unb --help

"""

# from django.core.management import execute_from_command_line
def execute_from_command_line(*args, **kwargs):
  print 'Not Implemented'

import os
import shutil
import subprocess
import sys

import argparse
from lib.commands.commands import arg, Group

import utils

import project
from config import config


# Utilities
# ---------

# TODO(nick): Currently this is unused.  We assume that the user has already
#   sourced the virtual environment.
def _source():
  """Add the virtual environment to the front of the system PATH."""
  venv = os.path.join(config.PROJECT_PATH, 'venv')
  if venv not in os.environ['PATH'].split(os.pathsep):
    os.environ['PATH'] = venv + os.pathsep + os.environ['PATH']


# Helpers
# -------

def _build_apidocs():
  # sphinx-apidoc: Build .rst docs from docstrings for all project modules.
  subprocess.call([
    'sphinx-apidoc',
    '--force',         # Overwrite existing files.
    '--module-first',  # Put module docs before submodule docs.
    # '--no-headings',   # Don't create headings
    '--separate',      # Create separate pages for each module
    '--output-dir',
    config.DOCS_MODULES_PATH,
    config.PROJECT_PATH,       # Directory containing modules to document.
    # exclude directories
    'management/setup',
    'setup.py',
  ])


def _build_docs():
  cwd = os.getcwd()  # get current directory
  try:
    os.chdir(config.DOCS_PATH)
    print 'Cleaning build directory... '
    try:
      shutil.rmtree(config.DOCS_BUILD_PATH)
    except OSError:
      # Catches the error when there is no build directory... This is not
      # foolproof.  For example it could also catch permissions errors.
      pass
    print 'Building docs...'
    # Inovke the Sphinx makefile to build the html documentation.
    subprocess.call(['make', 'html'])
  finally:
    os.chdir(cwd)


# Commands
# --------

def cli_init():
  """Project management utilities."""
  # Add the project path to sys.path for all utilities.
  sys.path.append(config.PROJECT_PATH)

  # Set the default environment settings to dev.
  os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        config.DEFAULT_DJANGO_SETTINGS_MODULE)

cli = Group(cli_init)


@arg('component', nargs='?')
def build(component=None):
  """Build script(s).

  Components may be built individually by passing a component name to this
  command.

      build       # Run all build scripts

      build docs  # Build the docs

      build js    # Build javascript files

      build css   # Build css files
  """
  components = {
    'docs': _build_docs
  }

  if not component:
    # Build all components
    components['docs']()
    # components[]()
  # elif component == 'frontend':
  #   # Build all frontend components
  #   components['js']()
  #   components['css']()
  else:
    # Build the specified component
    components[component]()
cli.command(build)


def deploy():
  """Deploy the project to various environments.

  This assumes that a git remote named "heroku" exists and points to the
  staging environment.
  """
  # Deploy to staging environment
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(
    ['heroku', 'run', './manage.py', 'migrate'])
cli.command(deploy)


@arg('name', nargs='?')
@arg('args', nargs=argparse.REMAINDER)
def m(name, args):
  """Run manage.py commands (using the dev environment settings)."""
  execute_from_command_line(sys.argv[1:], *args)
cli.command(m)


# TODO(nick): This should be a `run *` command that can run other things too.
def runserver():
  """Run the development server and restart on crash."""
  try:
    subprocess.call('\n'.join(['while true; do',
                               '  # re-start service',
                               '  echo "Starting Django Server"',
                               '  python manage.py runserver',
                               '  sleep 2',
                               'done']),
                    shell=True)
  except KeyboardInterrupt:
    pass
cli.command(runserver)


def lint():
  """Run linters."""
  subprocess.call('flake8')
cli.command(lint)


def test():
  """Run tests and linters."""
  subprocess.call('flake8')
  execute_from_command_line(['manage.py', 'test'])
cli.command(test)


def shell():
  """Run shell."""
  execute_from_command_line(['manage.py', 'shell_plus'])
cli.command(shell)


@arg('-v',
     '--verbose',
     action='store_false',
     help="Enable verbose output.")
def install_requirements(verbose=False):
  """pip install (dev-)requirements.txt"""

  def cmd(name):
    """Build the pip install command with appropriate options."""
    command = ['pip', 'install', '-r', name]
    if not verbose:
      command = command + ['-q']
    return command

  print 'Installing project dependencies...'
  subprocess.call(cmd(config.REQUIREMENTS_FILE_PATH))
  subprocess.call(cmd(config.DEV_REQUIREMENTS_FILE_PATH))
  # TODO(nick): Install npm dependencies per frontend project.
  #   $ npm install
cli.command(install_requirements, name='install-requirements')


def licenses():
  """List licenses of all 3rd party packages."""
  subprocess.call(['yolk', '-l', '-f', 'license'])
cli.command(licenses)


@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  if not os.path.isfile(config.VERSION_FILE_PATH):
    version = '0.0.0'
    version = utils.bump_version(version, part)
    utils.write_version(version)
  else:
    version = utils.read_version()
    version = utils.bump_version(version, part)
    utils.write_version(version)
cli.command(bump)


@arg('app_name')
def update_remote(app_name):
  """Update the Heroku git remote given a Heroku app name.

  Ensure the remote is set to use the ssh protocol, which also eliminates the
  need to specify the app name for each Heroku toolbelt command.
  """
  subprocess.call(['git', 'remote', 'rm', 'heroku'])
  subprocess.call(['heroku', 'git:remote', '-a', app_name, '--ssh-git'])
cli.command(update_remote, name='update-remote')


def migrate():
  """Make migrations and run them."""
  execute_from_command_line(['manage.py', 'makemigrations'])
  execute_from_command_line(['manage.py', 'migrate'])
cli.command(migrate)


def clear_cache():
  """Clear expired session data from the database-backed cache."""
  print 'Clearing database cache...'
  execute_from_command_line(['manage.py', 'clearsessions'])
cli.command(clear_cache, name='clear-cache')


def mkconfig():
  """Make the UNB CLI config directory structure."""
  project.make_config_dir()
cli.command(mkconfig)


def list_projects():
  """List projects configured to use UNB CLI."""
  projects = project.list_projects()
  projects.sort()
  if projects:
    print 'Projects(%s):' % len(projects)
    for project_name in projects:
      print '  - ', project_name
  else:
    print 'No projects found.'
cli.command(list_projects, name='list-projects')


def current_project():
  """Get the project the current working directory is in."""
  print project.get_project_name(project.current_project_path())
cli.command(current_project, name='current-project')
