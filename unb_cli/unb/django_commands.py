import os
import subprocess
import sys

import argparse
from lib.commands.commands import arg

from . import cli
from . import config


# Utilities
# ---------

def _execute_django_command(name=None, args=None):
  _source(site_packages=True)
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


# Virtual Environment Utilities
# =============================

# TODO(nick): Currently this is unused.  We assume that the user has already
#   sourced the virtual environment.
def _source(site_packages=True, venv=False):
  """Add the virtual environment to the front of the system PATH."""
  venv_path = _get_venv_path()
  if venv_path:

    if site_packages:
      venv_sp = os.path.join(venv_path, 'lib', 'python2.7', 'site-packages')
      if venv_sp not in sys.path:
        sys.path.insert(1, venv_sp)

    if venv:
      venv_bin = os.path.join(venv_path, 'bin')
      if venv_bin not in os.environ['PATH'].split(os.pathsep):
        os.environ['PATH'] = venv_bin + os.pathsep + os.environ['PATH']


# TODO(nick): Not really a Django command.  Move this somewhere else!
def _get_venv_path():
  venv = os.path.join(config.PROJECT_PATH, 'venv')
  if os.path.exists(venv):
    return venv
  return None


def _in_venv():
  # NOTE:
  # If you are using virtualenv (github.com/pypa/virtualenv), this answer is
  # equally correct for Python 2 or Python 3. If you are using pyvenv
  # (legacy.python.org/dev/peps/pep-0405), a virtualenv-equivalent built into
  # Python 3.3+ (but not the same thing as virtualenv), then it uses
  # sys.base_prefix instead of sys.real_prefix, and sys.base_prefix always
  # exists; outside a pyvenv it is equal to sys.prefix.
  return hasattr(sys, 'real_prefix')


# Commands to move somewhere else
# ===============================

# TODO(nick): Not really a Django command.  Move this somewhere else!
def test():
  """Run tests and linters."""
  # lint: from main.py  # TODO(nick): Move this into a library!
  if _in_project():
    subprocess.call(['flake8', config.PROJECT_PATH])
  # end lint
  _execute_django_command('test')
cli.register(test)


# TODO(nick): Not really a Django command.  Move this somewhere else!
def shell():
  """Run shell."""
  _execute_django_command('shell_plus')
cli.register(shell)


# Django Commands
# ===============

@arg('name', nargs='?',
     help="The name of the manage.py command you want to run.")
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def m(name, args):
  """Run manage.py commands (using the dev environment settings)."""
  _execute_django_command(name, args)
cli.register(m)


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
cli.register(runserver)


def migrate():
  """Make migrations and run them."""
  _execute_django_command('makemigrations')
  _execute_django_command('migrate')
cli.register(migrate)


def clear_cache():
  """Clear expired session data from the database-backed cache."""
  print 'Clearing database cache...'
  _execute_django_command('clearsessions')
cli.register(clear_cache, name='clear-cache')
