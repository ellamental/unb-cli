"""Read, write and bump version numbers."""

import os


def read(version_file_path, default=None):
  """Returns the version string as read from version_file.

  Args:
    version_file_path(str):  File path to read version from.  May be absolute
      or relative.
    default(str):  Version to use if the version file was not found.

  Returns (str) version or (None) if the file was not found and no default was
  provided.
  """
  if not os.path.isfile(version_file_path):
    return default
  with open(version_file_path) as f:
    return f.read().strip()


def write(version_file_path, version):
  """Writes a version string to version_file.

  Args:
    version(str):  The version as a string.
    version_file_path(str):  File path to write version to.
  """
  with open(version_file_path, 'wb') as f:
    f.write(version)


def bump(version, part='patch'):
  """Increments the `part` of a `version` by 1.

  Args:
    version(str):  The version string.
    part(str):  Which part of the version to bump 'major', 'minor', or 'patch'.

  Returns a string representing the bumpped version number.
  """
  major, minor, patch = _version_string_to_tuple(version)
  if not part or part == 'patch':
    patch += 1
  elif part == 'minor':
    minor += 1
  elif part == 'major':
    major += 1
  return _version_tuple_to_string((major, minor, patch))


def bump_file(version_file_path, part='patch', default='0.0.0'):
  """Utility function to read, bump and write a version to a version file.

  Args:
    version_file_path(str):  File path to write version to.
    part(str):  Which part of the version to bump 'major', 'minor', or 'patch'.
    default(str):  Version to use if the version file was not found.
  """
  v = read(version_file_path, default)
  v = bump(v, part)
  write(version_file_path, v)


def _version_string_to_tuple(version_string):
  """Convert a version_string to a tuple (major, minor, patch) of integers."""
  return (int(n) for n in version_string.split('.'))


def _version_tuple_to_string(version_tuple):
  """Convert a version_tuple (major, minor, patch) to a string."""
  return '.'.join((str(n) for n in version_tuple))
