import subprocess

from lib.commands.commands import Group


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
