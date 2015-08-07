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

from lib.commands.commands import arg

from unb_cli import version

from . import cli
from . import config


# Utilities
# ---------

def _in_project():
  # TODO(nick): Should be something like:
  # return '.git' in os.listdir(config.PROJECT_PATH)
  return config.PROJECT_PATH != config.HOME_PATH


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
cli.register(build)


def deploy():
  """Deploy the project to various environments.

  This assumes that a git remote named "heroku" exists and points to the
  staging environment.
  """
  # Deploy to staging environment
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(
    ['heroku', 'run', './manage.py', 'migrate'])
cli.register(deploy)


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
cli.register(lint)


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
cli.register(install_requirements, name='install-requirements')


def licenses():
  """List licenses of all 3rd party packages."""
  subprocess.call(['yolk', '-l', '-f', 'license'])
cli.register(licenses)


def get_version():
  """Get the version number of the current project."""
  v = version.read(config.VERSION_FILE_PATH)
  if v is not None:
    print v
cli.register(get_version, name='version')


@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  version.bump_file(config.VERSION_FILE_PATH, part, '0.0.0')
cli.register(bump)


@arg('app_name')
def update_remote(app_name):
  """Update the Heroku git remote given a Heroku app name.

  Ensure the remote is set to use the ssh protocol, which also eliminates the
  need to specify the app name for each Heroku toolbelt command.
  """
  subprocess.call(['git', 'remote', 'rm', 'heroku'])
  subprocess.call(['heroku', 'git:remote', '-a', app_name, '--ssh-git'])
cli.register(update_remote, name='update-remote')


@arg('key', nargs='?')
def conf(key):
  """Access config settings (mostly a debugging tool)."""
  if not key:
    from unb_cli import random_tools
    random_tools.pp(config)
  else:
    try:
      print "%s: %s" % (key, config[key])
    except KeyError:
      pass
cli.register(conf, 'config')
