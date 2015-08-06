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

import os
import shutil
import subprocess
import sys

import argparse
from lib.commands.commands import arg

from unb_cli import version

from . import cli
from . import config


# Utilities
# ---------

def _execute_django_command(name=None, args=None):
  _source()
  try:
    from django.core.management import execute_from_command_line
    name = name or 'help'
    args = args or []
    argv = ['manage.py', name] + args
    return execute_from_command_line(argv)
  except ImportError:
    cmd = ''
    if args:
      cmd = ' '.join([str(arg) for arg in args])
    print 'Not in a Django project.  Did not run command: %s' % cmd


def _in_project():
  return config.PROJECT_PATH != config.HOME_PATH


# TODO(nick): Currently this is unused.  We assume that the user has already
#   sourced the virtual environment.
def _source():
  """Add the virtual environment to the front of the system PATH."""
  venv = _get_venv()
  if venv:
    venv_bin = os.path.join(venv, 'bin')
    venv_sp = os.path.join(venv, 'lib', 'python2.7', 'site-packages')

    if venv_bin not in os.environ['PATH'].split(os.pathsep):
      os.environ['PATH'] = venv_bin + os.pathsep + os.environ['PATH']

    if venv_sp not in sys.path:
      sys.path.insert(1, venv_sp)


def _get_venv():
  venv = os.path.join(config.PROJECT_PATH, 'venv')
  if os.path.exists(venv):
    return venv
  return None


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


@arg('name', nargs='?',
     help="The name of the manage.py command you want to run.")
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def m(name, args):
  """Run manage.py commands (using the dev environment settings)."""
  _execute_django_command(name, args)
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
  """Run linters.

  Note:

  If you want a catch-all configuration, add a ``~/.config/flake8`` file.
  Here's an example.  This ignores some specific errors (E111: 4 space indent
  for example), and also excludes any directory in the project named ``venv``
  or ``migrations``.

      [flake8]
      ignore=E111,E121,F403
      exclude=migrations,venv
      max-line-length = 79

  For more info: https://flake8.readthedocs.org/en/2.0/config.html
  """
  if _in_project():
    subprocess.call(['flake8', config.PROJECT_PATH])
cli.command(lint)


def test():
  """Run tests and linters."""
  lint()
  _execute_django_command('test')
cli.command(test)


def shell():
  """Run shell."""
  _execute_django_command('shell_plus')
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


def get_version():
  """Get the version number of the current project."""
  v = version.read(config.VERSION_FILE_PATH)
  if v is not None:
    print v
cli.command(get_version, name='version')


@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  version.bump_file(config.VERSION_FILE_PATH, part, '0.0.0')
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
  _execute_django_command('makemigrations')
  _execute_django_command('migrate')
cli.command(migrate)


def clear_cache():
  """Clear expired session data from the database-backed cache."""
  print 'Clearing database cache...'
  _execute_django_command('clearsessions')
cli.command(clear_cache, name='clear-cache')
