import argparse
import subprocess

from lib.commands.commands import arg, Group


group = Group(
  title='Deploy the project to various environments.',
  description='Deploy the project to various environments.',
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


@group.command('shell')
def shell():
  """Run a Django shell on the default Heroku app."""
  subprocess.call(['heroku', 'run', './manage.py', 'shell_plus'])


@group.command('heroku')
def heroku():
  """Deploy to the Heroku app associated with a git remote named `heroku`.

  This assumes that a git remote named "heroku" exists.
  """
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(['heroku', 'run', './manage.py', 'migrate'])
