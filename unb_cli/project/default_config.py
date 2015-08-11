"""Default project config file values.

Args:

  overrides(dict):  A dict of user-defined configuration values (generally
    specified in ``~/.unb-cli.d/projects/project_name.py``) that will
    override the default values.

    Required Overrides:

      PROJECT_PATH
      APP_DIRNAME
"""

import os


ROOT_PATH = os.path.abspath(os.sep)
HOME_PATH = os.environ.get('HOME')

PROJECT_PATH = HOME_PATH

APP_DIRNAME = ''
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
