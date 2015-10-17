import os
import subprocess

from clams import arg, Command

from . import current_project


version = Command(
  name='version',
  title='Utilities for versioning and releases.',
  description='Utilities for versioning and releases.',
)


@version.register('bump')
@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version.bump_file(current_project().version_file_path, part, '0.0.0')


def _tag(version, message):
  """Create a git tag."""
  v = 'v' + version
  subprocess.call(['git', 'tag', '-a', v, '-m', message])


@version.register('tag')
@arg('message', nargs='?', default='')
def tag(message):
  """Create a git tag."""
  from unb_cli import version
  version_file_path = os.path.join(current_project().path,
                                   current_project().config.VERSION_FILENAME)
  v = version.read(version_file_path)
  _tag(v, message)


@version.register('version')
def get_version():
  """Get the version number of the current project."""
  from unb_cli import version
  v = version.read(current_project().version_file_path)
  if v is not None:
    print v
