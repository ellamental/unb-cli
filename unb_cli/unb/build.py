import os
import shutil
import subprocess

from lib.commands.commands import arg, Group

from . import current_project


group = Group(
  title='Build tools and scripts',
  description='Build tools and scripts',
)


@group.command(name='sphinx')
@arg('component', nargs='?')
def sphinx_docs(component=None):
  """Build Sphinx docs for a project."""
  cp = current_project()
  starting_directory = os.getcwd()  # get current directory
  try:
    docs_dir = os.path.join(cp.config.PROJECT_PATH, cp.config.DOCS_DIRNAME)
    os.chdir(docs_dir)
    print 'Cleaning build directory... '
    try:
      shutil.rmtree(os.path.join(docs_dir, cp.config.DOCS_BUILD_DIRNAME))
    except OSError:
      # Catches the error when there is no build directory... This is not
      # foolproof.  For example it could also catch permissions errors.
      pass
    print 'Building docs...'
    # Inovke the Sphinx makefile to build the html documentation.
    subprocess.call(['make', 'html'])
  finally:
    os.chdir(starting_directory)


@group.command(name='sphinx-api')
@arg('component', nargs='?')
def sphinx_api_docs(component=None):
  """Build Sphinx docs for a project."""
  cp = current_project()
  # sphinx-apidoc: Build .rst docs from docstrings for all project modules.
  docs_dir = os.path.join(cp.config.PROJECT_PATH, cp.config.DOCS_DIRNAME)
  docs_modules_dir = os.path.join(docs_dir, cp.config.DOCS_MODULES_DIRNAME)
  subprocess.call([
    'sphinx-apidoc',
    '--force',         # Overwrite existing files.
    '--module-first',  # Put module docs before submodule docs.
    # '--no-headings',   # Don't create headings
    '--separate',      # Create separate pages for each module
    '--output-dir',
    docs_modules_dir,
    cp.path,           # Directory containing modules to document.
    # exclude directories
    'management/setup',
    'setup.py',
  ])


@group.command(name='egg')
def py_egg():
  """Build a Python egg."""
  subprocess.call(['python', 'setup.py', 'sdist'])


# This might not work...
@group.command(name='egg-install')
def py_egg_install():
  """Install a Python egg locally (usually during development)."""
  subprocess.call(['pip', 'install', '-e', '.'])
