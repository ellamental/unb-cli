"""
Heroku Utilities
================

Heroku project/environment management tools.

"""

import argparse
import subprocess

from lib.commands.commands import arg, Group


group = Group(
  title='Heroku project/environment management tools',
  description='Heroku project/environment management tools',
)


@group.command('run')
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def run(args):
  """Run a command using `heroku run ./manage.py` on the default Heroku app."""
  base = ['heroku', 'run', './manage.py']
  subprocess.call(base + args)


@group.command('migrate')
def migrate():
  """Run migrations on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])


@group.command('push')
def push():
  """Deploy to the Heroku app associated with a git remote named `heroku`.

  This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])


@group.command('shell')
def shell():
  """Run a Django shell on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'shell_plus'])


@group.command('deploy')
def deploy():
  """Push/Migrate to the default Heroku app.

  See `push` and `migrate` for more information.


  NOTE: This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])
