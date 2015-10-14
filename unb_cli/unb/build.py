import os
import shutil
import subprocess

from clams import arg, Command

from . import current_project


build = Command(
  name='build',
  title='Build tools and scripts',
  description='Build tools and scripts',
)


@build.register('sphinx')
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
    # Run the doctests
    subprocess.call(['make', 'doctest'])
    # Inovke the Sphinx makefile to build the html documentation.
    subprocess.call(['make', 'html'])
  finally:
    os.chdir(starting_directory)


@build.register('sphinx-api')
@arg('component', nargs='?')
def sphinx_api_docs(component=None):
  """Generate Sphinx rst files for a project's api."""
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


@build.register('verify-docs')
def verify_docs():
  subprocess.call(['rest2html.py', 'README.txt'])
