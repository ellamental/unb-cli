import argparse
import logging
import imp
import os
import subprocess
import sys

from lib.commands.commands import arg, Group

from unb_cli.project import Project

import utilities


logger = logging.getLogger(__name__)


def current_project():
  return Project.get_from_path(os.getcwd())


def cli_init():
  """Project management utilities."""
  # TODO(nick): Don't forget to remove this code.
  # if cp.path:
  #   # Add the project path to sys.path for all utilities.
  #   if cp.path not in sys.path:
  #     sys.path.append(cp.path)

  cp = current_project()
  if utilities.is_django_project(cp.path):
    # Set the default settings module.
    # TODO(nick): This makes some pretty specific assumptions about a project's
    #   structure.  Maybe this should be configured explicitly in the project's
    #   config file?
    cp_settings = cp.config.APP_DIRNAME + '.settings.dev'

    default_settings = cp.config.get('DEFAULT_DJANGO_SETTINGS_MODULE',
                                     cp_settings)
    os.environ.setdefault(
      'DJANGO_SETTINGS_MODULE',
      default_settings)


cli = Group(cli_init)


# Each module under this exports ``group`` which is added here.
from . import build
cli.add_group(build.group, name='build')


from . import heroku
cli.add_group(heroku.group, name='heroku')


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
  cp = current_project()
  if utilities.is_django_project(cp.path):
    os.chdir(cp.path)
    subprocess.call(['./manage.py', 'shell_plus'])
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


@arg('name', nargs='?', default="",
     help="The name of the build.py command you want to run.")
@arg('args', nargs=argparse.REMAINDER,
     help="Arguments to pass to the build.py command.")
def b(name, args):
  """Execute functions contained in a project's project_root/build.py file."""
  cp = current_project()
  path = cp.path

  # Add the project path to sys.path
  sys.path.insert(0, path)

  build_file_path = os.path.join(path, 'build.py')
  if not os.path.exists(build_file_path):
    logger.info('No build script found.')
    return

  # build_script = imp.load_source('build_script', build_file_path)
  # method = getattr(build_script, name, None)

  build_methods = {}
  execfile(build_file_path, build_methods)
  print 'build_methods'
  print '============='
  for k, v in build_methods.items():
    if k != '__builtins__':
      print k + ':', v
  method = build_methods.get(name)

  if not method:
    logger.info('Method (%s) not found.', name)
    return

  method(*args)

cli.register(b)
