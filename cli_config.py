"""Configuration specific to the unb-cli tool."""

import os


UNB_CLI_D_DIRNAME = '.unb-cli.d'
PROJECTS_DIRNAME = 'projects'
CONFIG_FILENAME = 'config.py'
DEFAULT_CONFIG_DOTTED_PATH = 'config.defaults'
DEFAULT_CONFIG_MODULE_NAME = DEFAULT_CONFIG_DOTTED_PATH.split('.')[1]

ROOT_PATH = os.path.abspath(os.sep)
HOME_PATH = os.environ.get('HOME')
UNB_CLI_D_PATH = os.path.join(HOME_PATH, UNB_CLI_D_DIRNAME)
CONFIG_PATH = os.path.join(UNB_CLI_D_PATH, CONFIG_FILENAME)
PROJECTS_PATH = os.path.join(UNB_CLI_D_PATH, PROJECTS_DIRNAME)
