import logging
import os
import shutil

import jinja2

from unb_cli.config import cli


logger = logging.getLogger(__name__)


TEMPLATES_PATH = os.path.join(cli.UNB_CLI_D_PATH, 'templates')
CONFIG_FILENAME = '__config__.py'


def _template_path(name):
  template_path = os.path.join(TEMPLATES_PATH, name)
  if os.path.exists(template_path):
    return template_path


def _config_path(template_path):
  """Get the path of the config file stored at template_path."""
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


def _build_template(template_path, dest, config_path=None, overwrite=False,
                    no_render=False):
  logger.warning('Building template')
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
    logger.warning('Building path: %s', path)
    if path == CONFIG_FILENAME:
      continue

    # Get the full path to the source file
    source_path = os.path.join(template_path, path)

    # Process path by running it through the template engine.  This allows
    # users to build paths that contain config variables.  A common one is to
    # create a subdirectory named `app_name`.  This way the user can automate
    # the naming of directories by naming it `parent/{{app_name}}/`.
    path = jinja2.Template(path).render(env)
    dest_path = os.path.join(dest, path)

    # If this path is a directory, recursively build the template given the
    # initial config file as the rendering environment.
    if os.path.isdir(source_path):
      try:
        os.makedirs(dest_path)
      except OSError:
        pass
      if path == 'templates':
        # Django projects may contain templates that are meant to be rendered
        # by Django, NOT by this project builder.  By convention they're stored
        # in a directory named "templates".  This is a pretty horrible way of
        # checking if something is a template that shouldn't be rendered.
        # Another option might be to make this a config value... ignored_dirs
        # or something?
        # Here we just set a flag `no_render` that instructs future iterations
        # of this function not to try to render any file in this directory or
        # it's subdirectories.
        _build_template(source_path, dest_path, config_path=config_path,
                        overwrite=overwrite, no_render=True)
      else:
        _build_template(source_path, dest_path, config_path=config_path,
                        overwrite=overwrite, no_render=no_render)
    else:
      if no_render:
        shutil.copy(source_path, dest_path)
      else:
        rendered = loader.get_template(path).render(env)
        _write(rendered, dest_path, overwrite)


def build_template(name, dest, config_path=None, overwrite=False):
  template_path = _template_path(name)
  _build_template(template_path, dest, config_path, overwrite)
