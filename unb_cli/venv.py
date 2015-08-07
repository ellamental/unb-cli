"""Utilities for working with virtual environments."""

import sys


def in_venv():
  # NOTE:
  # If you are using virtualenv (github.com/pypa/virtualenv), this answer is
  # equally correct for Python 2 or Python 3. If you are using pyvenv
  # (legacy.python.org/dev/peps/pep-0405), a virtualenv-equivalent built into
  # Python 3.3+ (but not the same thing as virtualenv), then it uses
  # sys.base_prefix instead of sys.real_prefix, and sys.base_prefix always
  # exists; outside a pyvenv it is equal to sys.prefix.
  return hasattr(sys, 'real_prefix')
