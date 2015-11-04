import argparse
import logging
import imp
import os
import subprocess
import sys

from clams import arg, Command

from unb_cli.project import Project, is_project_root

import utilities


logger = logging.getLogger(__name__)


unb = Command('unb')


def current_project():
  return Project.get_from_path(os.getcwd())


@unb.register('b')
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


from . import django_commands
unb.add_subcommand(django_commands.dj)


from . import docs
unb.add_subcommand(docs.command)


from . import gemfury
unb.add_subcommand(gemfury.command)


from . import heroku
unb.add_subcommand(heroku.command)


@unb.register('lint')
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


from . import node
unb.add_subcommand(node.command)


from . import pip
unb.add_subcommand(pip.pip)


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


from . import project
unb.add_subcommand(project.project)


@unb.register('shell')
def shell():
  """Run a Python shell."""
  cp = current_project()
  if utilities.is_django_project(cp.path):
    os.chdir(cp.path)
    subprocess.call(['./manage.py', 'shell_plus'])
  else:
    subprocess.call(['ipython'])


from . import template
unb.add_subcommand(template.template)


from . import version
unb.add_subcommand(version.version)


def run():
  """Project management utilities."""

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

  unb.init()
  unb.parse_args()
