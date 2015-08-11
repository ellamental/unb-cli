import os
import subprocess
import sys

from lib.commands.commands import arg, Group

from unb_cli import project as project_lib


project_path = project_lib.find_parent_project_path(os.getcwd())
project_name = project_lib.get_project_name_from_path(project_path)
config_path = project_lib.config_path(project_name)
config = project_lib.config(config_path)


def _is_django_project():
  """A, not totally reliable, test if we're in a Django project."""
  managepy_path = os.path.join(config.PROJECT_PATH, 'manage.py')
  if os.path.exists(managepy_path):
    return True
  return False


def cli_init():
  """Project management utilities."""
  project_path = config.get('PROJECT_PATH', config.HOME_PATH)

  if project_path != config.HOME_PATH:
    # Add the project path to sys.path for all utilities.
    if config.PROJECT_PATH not in sys.path:
      sys.path.append(config.PROJECT_PATH)

  if _is_django_project():
    # Set the default settings module.
    os.environ.setdefault(
      'DJANGO_SETTINGS_MODULE',
      config.get('DEFAULT_DJANGO_SETTINGS_MODULE', 'settings'))


cli = Group(cli_init)


# Each module under this exports ``group`` which is added here.
from . import build
cli.add_group(build.group, name='build')


@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version.bump_file(config.VERSION_FILE_PATH, part, '0.0.0')
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
  subprocess.call(cmd(config.REQUIREMENTS_FILE_PATH))
  subprocess.call(cmd(config.DEV_REQUIREMENTS_FILE_PATH))
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
  project_path = project_lib.find_parent_project_path(os.getcwd())
  if project_path:
    subprocess.call(['flake8', project_path])
cli.register(lint)


import project
cli.add_group(project.group, name='project')


def shell():
  """Run shell."""
  if utilities.is_django_project(config.PROJECT_PATH):
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
  v = version.read(config.VERSION_FILE_PATH)
  if v is not None:
    print v
cli.register(get_version, name='version')
