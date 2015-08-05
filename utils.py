"""
Useful Management Utilities
===========================

A collection of management utilities that may be useful both in and outside the
management project.

"""

from config import config


def version_string_to_tuple(version_string):
  """Convert a version_string to a tuple (major, minor, patch) of integers."""
  return (int(n) for n in version_string.split('.'))


def version_tuple_to_string(version_tuple):
  """Convert a version_tuple (major, minor, patch) to a string."""
  return '.'.join((str(n) for n in version_tuple))


def read_version(version_filename=config.VERSION_FILE_PATH):
  """Returns the version string as read from version_file.

  Args:
    version_filename(str): Filename to read version from.
  """
  with open(version_filename) as f:
    return f.read().strip()


def write_version(version, version_filename=config.VERSION_FILE_PATH):
  """Writes a version string to version_file.

  Args:
    version(str): The version as a string.
    version_filename(str): Filename to write version to.
  """
  with open(version_filename, 'wb') as f:
    f.write(version)


def bump_version(version, part='patch'):
  """Increments the `part` of a `version` by 1.

  Args:
    version(str): The version string.
    part(str): Which part of the version to bump 'major', 'minor', or 'patch'.

  Returns:
    A string representing the bumpped version number.
  """
  major, minor, patch = version_string_to_tuple(version)
  if not part or part == 'patch':
    patch += 1
  elif part == 'minor':
    minor += 1
  elif part == 'major':
    major += 1
  return version_tuple_to_string((major, minor, patch))
