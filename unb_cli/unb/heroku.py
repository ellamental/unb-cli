"""
Heroku Utilities
================

Heroku project/environment management tools.

"""

import argparse
import subprocess

from clams import arg, Command


command = Command(
  name='heroku',
  title='Heroku project/environment management tools',
  description='Heroku project/environment management tools',
)


@command.register('deploy')
def deploy():
  """Push/Migrate to the default Heroku app.

  See `push` and `migrate` for more information.


  NOTE: This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])


@command.register('config-list')
def config_list():
  """Get a list of environment variable names/values."""
  subprocess.call(['heroku', 'config'])


@command.register('config-get')
@arg('var', help="Name of environment variable.")
def config_get(var):
  """Get the value of an environment variable."""
  subprocess.call(['heroku', 'config:get', var])


@command.register('config-set')
@arg('var', help="name=value")
def config_set(var):
  """Set an environment variable."""
  subprocess.call(['heroku', 'config:set', var])


@command.register('manage')
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def manage(args):
  """Run a command using `heroku run ./manage.py` on the default Heroku app."""
  base = ['heroku', 'run', './manage.py']
  subprocess.call(base + args)


@command.register('migrate')
def migrate():
  """Run migrations on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])


@command.register('push')
def push():
  """Deploy to the Heroku app associated with a git remote named `heroku`.

  This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])


@command.register('run')
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def run(args):
  """Run a command using `heroku run` on the default Heroku app."""
  base = ['heroku', 'run']
  subprocess.call(base + args)


@command.register('shell')
def shell():
  """Run a Django shell on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'shell_plus'])


@command.register('update-remote')
@arg('app_name')
def update_remote(app_name):
  """Update the Heroku git remote given a Heroku app name.

  Ensure the remote is set to use the ssh protocol, which also eliminates the
  need to specify the app name for each Heroku toolbelt command.
  """
  subprocess.call(['git', 'remote', 'rm', 'heroku'])
  subprocess.call(['heroku', 'git:remote', '-a', app_name, '--ssh-git'])
