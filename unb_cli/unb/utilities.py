import logging
import os
import sys

from contextlib import contextmanager


logger = logging.getLogger(__name__)


@contextmanager
def push_sys_path(path):
  sys.path.insert(0, path)
  yield
  sys.path.pop(0)


def is_django_project(path):
  cwd = os.getcwd()
  while True:
    if os.path.exists(os.path.join(cwd, 'manage.py')):
      return True
    if cwd == path or cwd == os.path.sep:
      return False
    cwd = os.path.dirname(cwd)
  return False
