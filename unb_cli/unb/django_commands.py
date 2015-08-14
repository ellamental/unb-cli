from functools import wraps
import logging
import os
import subprocess
import sys

import argparse
from lib.commands.commands import arg, Group

import utilities

from . import current_project


logger = logging.getLogger(__name__)


group = Group(
  title='Django commands and tasks.',
  description='Django commands and tasks.',
)


# Django Command Utilities
# ========================


def _django_command(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not utilities.is_django_project(current_project().path):
      print 'Error: Not in a Django project.'
      return
    else:
      return func(*args, **kwargs)
  return wrapper


def _execute_django_command(name=None, args=None):
  cp = current_project()
  args = args or []
  name = name or 'help'

  cmd = ' '.join([str(arg) for arg in args])
  utilities.activate_virtualenv(cp.path)
  try:
    from django.core.management import execute_from_command_line
  except ImportError:
    print 'Not in a Django project.  Did not run command: %s' % cmd
    return

  argv = ['manage.py', name] + args
  with utilities.push_sys_path(cp.path):
    execute_from_command_line(argv)


# Django Commands
# ===============

@group.command()
@_django_command
@arg('name', nargs='?',
     help="The name of the manage.py command you want to run.")
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def m(name, args):
  """Run manage.py commands (using the dev environment settings)."""
  _execute_django_command(name, args)


@group.command(name='run')
@_django_command
def runserver():
  """Run the development server and restart on crash."""
  import traceback
  import time
  os.chdir(current_project().path)
  while True:
    try:
      # runserver does a sys.exit() on C-c so we don't have to special-case it
      _execute_django_command('runserver')
    except Exception:
      print traceback.format_exc()
    time.sleep(2)
  sys.exit()


@group.command()
@_django_command
def migrate():
  """Make migrations and run them."""
  _execute_django_command('makemigrations')
  _execute_django_command('migrate')


@group.command(name='clear-cache')
@_django_command
def clear_cache():
  """Clear expired session data from the database-backed cache."""
  _execute_django_command('clearsessions')


# Commands to move somewhere else
# ===============================

# TODO(nick): Not really a Django command.  Move this somewhere else!
@group.command()
@_django_command
def test():
  """Run tests and linters."""
  # lint: from main.py  # TODO(nick): Move this into a library!
  subprocess.call(['flake8', current_project().path])
  # end lint
  _execute_django_command('test')
