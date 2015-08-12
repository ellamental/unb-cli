import os
import sys

from contextlib import contextmanager


@contextmanager
def push_sys_path(path):
  sys.path.insert(0, path)
  yield
  sys.path.pop(0)


def is_project(project_path):
  return config.PROJECT_PATH != config.HOME_PATH


def is_django_project(project_path):
  return os.path.exists(os.path.join(project_path, 'manage.py'))


def activate_virtualenv(path):
  activate_this = os.path.join(path, 'venv', 'bin', 'activate_this.py')
  if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))


# Utilities
# =========

