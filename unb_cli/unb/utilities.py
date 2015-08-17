import os
import sys

from contextlib import contextmanager


@contextmanager
def push_sys_path(path):
  sys.path.insert(0, path)
  yield
  sys.path.pop(0)


def is_django_project(path):
  if os.path.exists(os.path.join(path, 'manage.py')):
    return True
  else:
    subdirs = [x[0] for x in os.walk(path)]
    for subdir in subdirs:
      subpath = os.path.join(path, subdir)
      if os.path.exists(os.path.join(subpath, 'manage.py')):
        return True
  return False


def activate_virtualenv(path):
  if path:
    activate_this = os.path.join(path, 'venv', 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
      execfile(activate_this, dict(__file__=activate_this))
