"""
import template

loader = template.loader('project_template')

loader.render_project(overwrite=False)



from unb_cli import template


unb new template name  #==> creates a new template at ~/.unb-cli/templates/name

unb new py-project name
#==> create name/ in current directory
#==> copy py-project default config file (found where py-project registered)
#==> cd to name/  (with switch to not cd for use in other commands)

edit config

unb create-project #optional path-to-config-file(default cwd)



.unb-cli.d/templates/project-name/config.py

"""

import logging
import os
import shutil

import jinja2

from unb_cli.config import cli


logger = logging.getLogger(__name__)


TEMPLATES_PATH = os.path.join(cli.UNB_CLI_D_PATH, 'templates')
CONFIG_FILENAME = 'config.py'


def _template_path(name):
  template_path = os.path.join(TEMPLATES_PATH, name)
  if os.path.exists(template_path):
    return template_path


def _config_path(template_path):
  config_path = os.path.join(template_path, CONFIG_FILENAME)
  if os.path.exists(config_path):
    return config_path


def _loader(path):
  return jinja2.Environment(
    loader=jinja2.FileSystemLoader(path),
    keep_trailing_newline=True,
    autoescape=False,
  )


def _load_config(path):
  ret = {}
  execfile(path, ret)
  del ret['__builtins__']
  return ret


def _write(text, path, overwrite=False):
  if os.path.exists(path) and overwrite is False:
    logger.info('Path exists and overwrite is False: %s', path)
    return
  with open(path, 'w') as f:
    logger.info('Rendering template to: %s', path)
    f.write(text)


def list_templates():
  """List the currently available templates."""
  return os.listdir(TEMPLATES_PATH)


def new_template(name):
  """Create a new template directory with config at unb-cli.d/templates/name.

  Raises:
    OSError: If template directory exists.
  """
  template_path = _template_path(name)
  config_path = _config_path(template_path)
  default_config_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'default_config.py')
  logger.info('Creating template directory at: %s', template_path)
  os.makedirs(template_path)  # Raises OSError if path exists
  shutil.copy(default_config_path, config_path)
  return template_path


def copy_config(template_name, dest):
  config_path = _config_path(_template_path(template_name))
  if config_path:
    logger.info('Copy config file from %s to %s', config_path, dest)
    shutil.copy(config_path, dest)
    return dest


def _build_template(template_path, dest, config_path=None, overwrite=False):
  import markup
  from library import wrap, wrap_block, pystr

  default_env = {
    'markup': markup,
    'wrap': wrap,
    'wrap_block': wrap_block,
    'pystr': pystr,
  }

  if config_path is None:
    config_path = _config_path(dest)

  loader = _loader(template_path)
  env = dict(default_env, **_load_config(config_path))

  paths = os.listdir(template_path)
  for path in paths:
    if path == 'config.py':
      continue
    full_template_path = os.path.join(template_path, path)
    dest_path = os.path.join(dest, path)
    if not os.path.isdir(full_template_path):
      rendered = loader.get_template(path).render(env)
      _write(rendered, dest_path, overwrite)
    else:
      subdir_config_path = _config_path(full_template_path)
      if subdir_config_path:
        config_path = subdir_config_path
      _build_template(full_template_path, dest_path, config_path=config_path,
                      overwrite=overwrite)


def build_template(name, dest, config_path=None, overwrite=False):
  template_path = _template_path(name)
  _build_template(template_path, dest, config_path, overwrite)
