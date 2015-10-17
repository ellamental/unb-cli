import os
import shutil
import subprocess

from clams import arg, Command

from . import current_project


command = Command(
  name='docs',
  title='Documentation tools.',
  description='Documentation tools.',
)


@command.register('build')
def build():
  """Build Sphinx docs for a project."""
  cp = current_project()
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


@command.register('sphinx-api')
def sphinx_api():
  """Generate Sphinx rst files for a project's api.

  See: http://sphinx-doc.org/ext/autodoc.html#module-sphinx.ext.autodoc
  """
  cp = current_project()
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
    # exclude directories/filenames
    'setup.py',
  ])


@command.register('verify')
def verify():
  subprocess.call(['rest2html.py', 'README.txt'])
