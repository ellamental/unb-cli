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
    docs_dir = os.path.join(cp.path, cp.config.DOCS_DIRNAME)
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
  docs_dir = os.path.join(cp.path, cp.config.DOCS_DIRNAME)
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
  subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel'])


@group.command(name='package')
@arg('dist', help=("Package version (example: `0.0.3*`).  Use matching to "
                   "upload multiple versions (source dist and a wheel, for "
                   "example)."))
@arg('-r', help=("Repository to upload to.  Common ones include, `pypi` and "
                 "`testpypi` (they are defined in your `~/.pypirc`)."))
def package(dist, repo):
  """Build and upload a Python package.

  Requires [twine](https://pypi.python.org/pypi/twine).
  """
  subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel'])
  dist_version = 'dist/' + dist
  twine_command = ['twine', 'upload', dist_version]
  if repo:
     twine_command.append('-r')
     twine_command.append(repo)
  subprocess.call(twine_command)


# This might not work...
@group.command(name='egg-install')
def py_egg_install():
  """Install a Python egg locally (usually during development)."""
  subprocess.call(['pip', 'install', '-e', '.'])


@group.command(name='verify-docs')
def verify_docs():
  subprocess.call(['rest2html.py', 'README.txt'])
