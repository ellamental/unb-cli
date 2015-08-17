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

# More-or-Less Standard Locations
# ===============================

# Sphinx Documentation Settings
# -----------------------------

DOCS_DIRNAME = 'docs'
DOCS_BUILD_DIRNAME = '.build'
DOCS_MODULES_DIRNAME = 'modules'

# Versioning
# ----------

VERSION_FILENAME = 'VERSION'

# Project Dependencies / Requirements Files
# -----------------------------------------

REQUIREMENTS_FILENAME = 'requirements.txt'
DEV_REQUIREMENTS_FILENAME = 'dev-requirements.txt'
