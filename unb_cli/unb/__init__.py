import os
import subprocess
import sys

from lib.commands.commands import arg, Group

from unb_cli.project import Project


def current_project():
  return Project.get_from_path(os.getcwd())


def _is_django_project():
  """A, not totally reliable, test if we're in a Django project."""
  managepy_path = os.path.join(current_project().path, 'manage.py')
  if os.path.exists(managepy_path):
    return True
  return False


def cli_init():
  """Project management utilities."""
  cp = current_project()
  if cp.path:
    # Add the project path to sys.path for all utilities.
    if cp.path not in sys.path:
      sys.path.append(cp.path)

  if _is_django_project():
    # Set the default settings module.
    os.environ.setdefault(
      'DJANGO_SETTINGS_MODULE',
      cp.config.get('DEFAULT_DJANGO_SETTINGS_MODULE', 'settings'))


cli = Group(cli_init)


# Each module under this exports ``group`` which is added here.
from . import build
cli.add_group(build.group, name='build')


@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version.bump_file(current_project().config.VERSION_FILE_PATH, part, '0.0.0')
cli.register(bump)


from . import deploy
cli.add_group(deploy.group, name='deploy')


from . import django_commands
cli.add_group(django_commands.group, name='dj')


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
  cp = current_project()
  subprocess.call(cmd(cp.config.REQUIREMENTS_FILE_PATH))
  subprocess.call(cmd(cp.config.DEV_REQUIREMENTS_FILE_PATH))
  # TODO(nick): Install npm dependencies per frontend project.
  #   $ npm install
cli.register(install_requirements, name='install-requirements')


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
  path = current_project().path
  if path:
    subprocess.call(['flake8', path])
cli.register(lint)


def prettify(src, dest):
  """Prettify html."""
  # TODO(nick): pip install beautifulsoup4
  if os.path.exists(dest):
    answer = raw_input('Overwrite file %s? (y/n)' % dest)
    if answer != 'y':
      print 'Operation canceled.'
      return
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(open(src))
  with open(dest, 'w') as f:
    f.write(soup.prettify(formatter="html"))


import project
cli.add_group(project.group, name='project')


def shell():
  """Run shell."""
  import utilities
  if utilities.is_django_project(current_project().path):
    import django_commands
    django_commands._execute_django_command('shell_plus')
  else:
    subprocess.call(['ipython'])
cli.register(shell)


from . import template
cli.add_group(template.group, name='template')


@arg('app_name')
def update_remote(app_name):
  """Update the Heroku git remote given a Heroku app name.

  Ensure the remote is set to use the ssh protocol, which also eliminates the
  need to specify the app name for each Heroku toolbelt command.
  """
  subprocess.call(['git', 'remote', 'rm', 'heroku'])
  subprocess.call(['heroku', 'git:remote', '-a', app_name, '--ssh-git'])
cli.register(update_remote, name='update-remote')


def get_version():
  """Get the version number of the current project."""
  from unb_cli import version
  v = version.read(current_project().config.VERSION_FILE_PATH)
  if v is not None:
    print v
cli.register(get_version, name='version')


def install():
  """Print the command to pip install unb-cli from source."""
  # TODO(nick): This is pretty fragile.  If the user names this project
  #   anything else, this command breaks.
  path = Project.get_from_name('unb-cli').path
  if path:
    subprocess.call(['pip', 'install', '-e', path])
  else:
    print 'cd unb-cli-directory'
    print 'pip install -e .'
cli.register(install)
