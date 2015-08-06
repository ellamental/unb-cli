import sys

import cli_config as cfg
from . import utils


# TODO(nick): Don't do this on import!
sys.path.append(cfg.UNB_CLI_D_PATH)

# TODO(nick): Don't do this on import!
config = utils.get_current_config()
