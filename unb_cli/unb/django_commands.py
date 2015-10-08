import argparse
from functools import wraps
import logging
import os
import subprocess
import sys

from clams import arg, Command
import utilities

from . import current_project


logger = logging.getLogger(__name__)


dj = Command(
  name='dj',
  title='Django commands and tasks.',
  description='Django commands and tasks.',
)


# Django Command Utilities
# ========================


def _django_dir(path):
  if os.path.exists(os.path.join(path, 'manage.py')):
    return path
  else:
    for name in os.listdir(path):
      subpath = os.path.join(path, name)
      if os.path.isdir(subpath):
        if os.path.exists(os.path.join(subpath, 'manage.py')):
          return subpath
  return None


def _django_command(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not _django_dir(current_project().path):
      print 'Error: Not in a Django project.'
      return
    else:
      return func(*args, **kwargs)
  return wrapper


def _execute_django_command(name=None, *args):
  name = name or 'help'
  cp = current_project()
  cp.activate_venv()

  try:
    from django.core.management import execute_from_command_line
  except ImportError:
    cmd = ' '.join([str(arg) for arg in args])
    print 'Failed to import Django.  Did not run command: %s' % cmd
    print 'Have you activated the virtual environment and installed Django?'
    return

  argv = ['manage.py', name] + list(args)
  djdir = _django_dir(cp.path)
  with utilities.push_sys_path(djdir):
    execute_from_command_line(argv)


# Django Commands
# ===============

@dj.register('m')
@_django_command
@arg('name', nargs='?',
     help="The name of the manage.py command you want to run.")
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def m(name, args):
  """Run manage.py commands (using the dev environment settings)."""
  _execute_django_command(name, *args)


@dj.register('run')
@_django_command
def runserver():
  """Run the development server and restart on crash."""
  import traceback
  import time
  os.chdir(_django_dir(current_project().path))
  while True:
    try:
      # runserver does a sys.exit() on C-c so we don't have to special-case it
      _execute_django_command('runserver')
    except Exception:
      print traceback.format_exc()
    time.sleep(2)
  sys.exit()


@dj.register('migrate')
@_django_command
def migrate():
  """Make migrations and run them."""
  _execute_django_command('makemigrations')
  _execute_django_command('migrate')


@dj.register('clear-cache')
@_django_command
def clear_cache():
  """Clear expired session data from the database-backed cache."""
  _execute_django_command('clearsessions')


# Commands to move somewhere else
# ===============================

# TODO(nick): Not really a Django command.  Move this somewhere else!
@dj.register('test')
@_django_command
def test():
  """Run tests and linters."""
  # lint: from main.py  # TODO(nick): Move this into a library!
  subprocess.call(['flake8', current_project().path])
  # end lint
  _execute_django_command('test')
