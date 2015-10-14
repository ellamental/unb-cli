import os
import subprocess

from clams import arg, Command

from unb_cli.project import is_project_root


pip = Command(
  name='pip',
  title='pip interface and tools',
  description='pip interface and tools',
)


@pip.register('install')
@arg('package', nargs='?', default='requirements.txt')
@arg('--nocache', action='store_true',
     help="Don't use pip's cache (fetch all packages from server).")
@arg('-v', '--verbose', action='store_true', help="Enable verbose output.")
def install(package, nocache, verbose):
  """Install package or packages from a requirements file.

  If `package` ends with `.txt` then `pip install -r package` is used.  If
  `package` is not supplied, it defaults to `requirements.txt`.

  """
  if package.endswith('.txt'):
    command = ['pip', 'install', '-r', package]
    if not verbose:
      command = command + ['-q']

    # Find the file!  It might not be in the current directory.
    while True:
      path = os.getcwd()
      if os.path.exists(package):
        print 'Installing packages from %s' % os.path.join(path, package)
        subprocess.call(command)
        break
      if is_project_root(path) or path == os.path.abspath(os.sep):
        print "%s not found in project." % package
        break
      os.chdir(os.pardir)
  else:
    subprocess.call(['pip', 'install', package])


@pip.register('install-local')
def install_local():
  """Install a Python egg locally (usually during development)."""
  subprocess.call(['pip', 'install', '-e', '.'])


@pip.register('uninstall')
@arg('package')
def uninstall(package):
  """Uninstall a package using pip."""

  subprocess.call(['pip', 'uninstall', package])


@pip.register('build')
def build():
  """Build a Python egg."""
  subprocess.call(['python', 'setup.py', 'sdist', 'bdist_wheel'])


@pip.register('upload')
@arg('dist', help=("Package version (example: `0.0.3`).  `*` will be appended "
                   "to upload all versions (source dist and a wheel, for "
                   "example)."))
@arg('repo', help=("Repository to upload to.  Common ones include, `pypi` and "
                   "`testpypi` (they are defined in your `~/.pypirc`)."))
def upload(dist, repo):
  """Upload a pre-built Python package.

  Requires [twine](https://pypi.python.org/pypi/twine).
  """
  # TODO(nick): `cd $PROJECT_ROOT` first.
  dist_version = 'dist/' + '*' + dist + '*'
  twine_command = ['twine', 'upload', dist_version, '-r', repo]
  subprocess.call(twine_command)
