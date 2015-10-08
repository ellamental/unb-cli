"""
Heroku Utilities
================

Heroku project/environment management tools.

"""

import argparse
import subprocess

from clams import arg, Command


heroku = Command(
  name='heroku',
  title='Heroku project/environment management tools',
  description='Heroku project/environment management tools',
)


@heroku.register('run')
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def run(args):
  """Run a command using `heroku run ./manage.py` on the default Heroku app."""
  base = ['heroku', 'run', './manage.py']
  subprocess.call(base + args)


@heroku.register('migrate')
def migrate():
  """Run migrations on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])


@heroku.register('push')
def push():
  """Deploy to the Heroku app associated with a git remote named `heroku`.

  This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])


@heroku.register('shell')
def shell():
  """Run a Django shell on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'shell_plus'])


@heroku.register('deploy')
def deploy():
  """Push/Migrate to the default Heroku app.

  See `push` and `migrate` for more information.


  NOTE: This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])
