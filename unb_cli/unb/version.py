import os
import subprocess

from clams import arg, Command

from . import current_project


version = Command(
  name='version',
  title='Utilities for versioning and releases.',
  description='Utilities for versioning and releases.',
)


def _get_version():
    """Read and return the project version number."""
    from unb_cli import version
    v = version.read(current_project().version_file_path)
    return v or ''


def _list_tags():
  """List tags."""
  subprocess.call(['git', 'tag', '-l', '-n'])


def _tag(name, message, prefix='', suffix=''):
  """Create a git tag.

  Parameters
  ----------
  name : str
      The name of the tag to create
  message : str
      A short message about the tag
  prefix : str
      A prefix to add to the name
  suffix : str
      A suffix to add to the name

  Returns
  -------
  None

  """
  name = prefix + name + suffix
  subprocess.call(['git', 'tag', '-a', name, '-m', message])


def _push_tags():
  """Run `git push --follow-tags`."""
  subprocess.call(['git', 'push', '--follow-tags'])


@version.register('bump')
@arg('part', nargs='?', default='patch')
def bump(part):
  """Bump the version number."""
  from unb_cli import version
  version.bump_file(current_project().version_file_path, part, '0.0.0')


@version.register('tag')
@arg('message', nargs='?', default='',
     help='Annotate the tag with a message.')
@arg('--name', nargs='?', default='',
     help='Specify a tag name explicitly.')
@arg('--prefix', nargs='?', default='',
     help="""A prefix to add to the name.

     This is most useful when the name parameter is omitted.  For example, if
     the current version number were 1.2.3, ``unb version tag --prefix=v``
     would produce a tag named ``v1.2.3``.""")
@arg('--suffix', nargs='?', default='',
     help="""A suffix to add to the name.

     This is most useful when the name parameter is omitted.  For example, if
     the current version number were 1.2.3, ``unb version tag --suffix=-dev``
     would produce a tag named ``1.2.3-dev``.""")
def tag(message, name, prefix, suffix):
  """Create a git tag.

  If the tag name is not given explicitly, its name will equal the contents of
  the file project_root/VERSION.

  """
  if not name:
      name = _get_version()
  _tag(name, message, prefix, suffix)


@version.register('push-tags')
def push_tags():
  """Push and follow tags.  (`git push --follow-tags`)"""
  _push_tags()


@version.register('list-tags')
def list_tags():
  """List git tags."""
  _list_tags()


@version.register('version')
def get_version():
  """Get the version number of the current project."""
  print _get_version()
