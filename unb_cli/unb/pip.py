import os
import subprocess

from clams import arg, Command

from unb_cli.project import is_project_root


pip = Command('pip')

# group = Group(
#   title='pip interface and tools',
#   description='pip interface and tools',
# )


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
        subprocess.call(command)
        print 'Installed packages from %s' % os.path.join(path, package)
        break
      if is_project_root(path) or path == os.path.abspath(os.sep):
        print "%s not found in project." % package
        break
      os.chdir(os.pardir)
  else:
    subprocess.call(['pip', 'install', package])


@pip.register('uninstall')
@arg('package')
def uninstall(package):
  """Uninstall a package using pip."""

  subprocess.call(['pip', 'uninstall', package])
