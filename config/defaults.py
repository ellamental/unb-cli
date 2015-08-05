"""
Default Project-Agnostic configuration for unb-cli
==================================================

"""

import os


# Required Project Paths
# ======================

def _clean_config_dict(d):
  return {k: v for k, v in d.items() if k.isupper() and not k.startswith('_')}


def merge_overrides(overrides):
  """Returns a dict of config values.

  Args:

    overrides(dict):  A dict of user-defined configuration values (generally
      specified in ``~/.unb-cli.d/projects/project_name.py``) that will
      override the default values.

      Required Overrides:

        PROJECT_PATH
        APP_DIRNAME
  """
  overrides = _clean_config_dict(overrides)

  PROJECT_PATH = overrides['PROJECT_PATH']

  APP_DIRNAME = overrides['APP_DIRNAME']
  APP_PATH = os.path.join(PROJECT_PATH, APP_DIRNAME)

  # More-or-Less Standard Locations
  # ===============================

  # Sphinx Documentation Settings
  # -----------------------------

  DOCS_DIRNAME = 'docs'
  DOCS_PATH = os.path.join(PROJECT_PATH, DOCS_DIRNAME)

  DOCS_BUILD_DIRNAME = '.build'
  DOCS_BUILD_PATH = os.path.join(DOCS_PATH, DOCS_BUILD_DIRNAME)

  DOCS_MODULES_DIRNAME = 'modules'
  DOCS_MODULES_PATH = os.path.join(DOCS_PATH, DOCS_MODULES_DIRNAME)

  # Versioning
  # ----------

  VERSION_FILENAME = 'VERSION'
  VERSION_FILE_PATH = os.path.join(PROJECT_PATH, VERSION_FILENAME)

  # Project Dependencies / Requirements Files
  # -----------------------------------------

  REQUIREMENTS_FILENAME = 'requirements.txt'
  REQUIREMENTS_FILE_PATH = os.path.join(PROJECT_PATH, REQUIREMENTS_FILENAME)

  DEV_REQUIREMENTS_FILENAME = 'dev-requirements.txt'
  DEV_REQUIREMENTS_FILE_PATH = os.path.join(PROJECT_PATH,
                                            DEV_REQUIREMENTS_FILENAME)

  ret = locals()
  ret.update(overrides)
  return _clean_config_dict(ret)
