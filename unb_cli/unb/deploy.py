import argparse
import subprocess

from lib.commands.commands import arg, Group


group = Group(
  title='Deploy the project to various environments.',
  description='Deploy the project to various environments.',
)


@group.command('staging')
def staging():
  """Deploy to the default Heroku remote.

  This assumes that a git remote named "heroku" exists and points to the
  staging environment.
  """
  # Deploy to staging environment
  subprocess.call(['git', 'push', 'heroku', 'master'])
  subprocess.call(
    ['heroku', 'run', './manage.py', 'migrate'])


@group.command('run')
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the manage.py command.")
def run(args):
  """Run a command using `heroku run ./manage.py` on the default Heroku app."""
  base = ['heroku', 'run', './manage.py']
  subprocess.call(base + args)
