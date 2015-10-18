import os
import subprocess

from clams import arg, Command


command = Command(
  name='node',
  title='node.js tools',
  description='node.js tools',
)


# Stuff that belongs in unb_cli/node.py
# -------------------------------------

def _install():
  """Run `npm install`."""
  print 'Running `npm install`...'
  subprocess.call(['npm', 'install'])


def _link_lib():
  """Add a symlink from node_modules to js/lib."""
  print 'Symlinking node_modules/lib to js/lib...'
  os.chdir('node_modules')
  symlink_source = os.path.join('..', 'js', 'lib')
  symlink_dest = 'lib'
  if os.path.lexists(symlink_dest):
    print 'symlink exists, removing...'
    os.remove(symlink_dest)
  os.symlink(symlink_source, symlink_dest)


def _reset():
  """Remove the node_modules directory, reinstall and re-symlink lib."""
  print 'Trashing node_modules...'
  subprocess.call(['trash', 'node_modules'])
  _install()
  _link_lib()


# Commands
# --------

@command.register('install')
def install():
  """Run `npm install`."""
  _install()


@command.register('set-env')
@arg('-p', '--production', action='store_true',
     help='Set the environment to "production".')
@arg('-d', '--development', action='store_true',
     help='Set the environment to "development".')
def set_env(production, development):
  """This won't actually work... It will just print the string to eval."""
  if production:
    print 'export NODE_ENV=production'
  if development:
    print 'export NODE_ENV=development'
  if not production and not development:
    print 'export NODE_ENV=production'
    print 'export NODE_ENV=development'


@command.register('link-lib')
def link_lib():
  """Add a symlink from node_modules to js/lib."""
  _link_lib()


@command.register('reset')
def reset():
  """Remove the node_modules directory, reinstall and re-symlink lib."""
  _reset()


@command.register('watch')
def watch():
  """Run gulp watch."""
  subprocess.call(['gulp'])


@command.register('build')
def build():
  """Run gulp build."""
  subprocess.call(['gulp', 'build'])


@command.register('lint')
def lint():
  """Run gulp lint."""
  subprocess.call(['gulp', 'lint'])
