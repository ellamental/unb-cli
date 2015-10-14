import logging
import os
import shutil

import jinja2

from unb_cli import project


logger = logging.getLogger(__name__)


TEMPLATES_PATH = os.path.join(project.UNB_CLI_D_PATH, 'templates')
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
    block_start_string='{%%',
    block_end_string='%%}',
    variable_start_string='{{{{',
    variable_end_string='}}}}',
    comment_start_string='{##',
    comment_end_string='##}',
    line_statement_prefix='$$',
    line_comment_prefix='@@',
  )


def _load_config(path):
  ret = {}
  execfile(path, ret)
  del ret['__builtins__']
  return ret


def _get_env(config_path):
  import markup
  from library import wrap, wrap_block, pystr, camel_case

  default_env = {
    'camel_case': camel_case,
    'markup': markup,
    'pystr': pystr,
    'wrap': wrap,
    'wrap_block': wrap_block,
  }

  return dict(default_env, **_load_config(config_path))


def _write(text, path, overwrite=False):
  if os.path.exists(path) and overwrite is False:
    logger.info('Path exists and overwrite is False: %s', path)
    return
  with open(path, 'w') as f:
    logger.info('Rendering template to: %s', path)
    f.write(text)


def _copy(source, dest, overwrite=False):
  if os.path.exists(dest) and overwrite is False:
    logger.info('Path exists and overwrite is False: %s', dest)
    return
  logger.info('Copying file to: %s', dest)
  shutil.copy(source, dest)


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
  SKIP_COMPLETELY = (
    CONFIG_FILENAME,
    '.DS_Store',
    '.pyc',
  )

  COPY_ONLY_PATHS = (
    # Font files
    '.otf',
    '.eot',
    '.svg',
    '.ttf',
    '.woff',
    '.woff2',
    # Image files
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
  )

  if config_path is None:
    config_path = _config_path(dest)

  loader = _loader(template_path)
  env = _get_env(config_path)

  paths = os.listdir(template_path)
  for path in paths:
    if path.endswith(SKIP_COMPLETELY):
      continue

    # Get the full path to the source file
    source_path = os.path.join(template_path, path)

    # Process path by running it through the template engine.  This allows
    # users to build paths that contain config variables.  A common one is to
    # create a subdirectory named `app_name`.  This way the user can automate
    # the naming of directories by naming it `parent/{{app_name}}/`.
    rendered_path = loader.from_string(path).render(env)
    dest_path = os.path.join(dest, rendered_path)

    # If this path is a directory, recursively build the template given the
    # initial config file as the rendering environment.
    if os.path.isdir(source_path):
      try:
        os.makedirs(dest_path)
      except OSError:
        pass
      _build_template(source_path, dest_path, config_path=config_path,
                      overwrite=overwrite)
    else:
      if path.endswith(COPY_ONLY_PATHS):
        # Some filetypes cause problems when rendering (like encoding errors).
        # For those, just copy the file instead of rendering it.
        _copy(source_path, dest_path, overwrite)
      else:
        rendered = loader.get_template(path).render(env)
        _write(rendered, dest_path, overwrite)


def build_template(dest, config_path=None, overwrite=False):
  """Build a template, given a config file in the current working directory.

  If either `before` or `after` functions are defined in the config file, they
  will be run before and after the full template has rendered (respectively).
  These functions provide a convenient method for template authors to run
  common operations, such as running build or install scripts after the
  template has been rendered.
  """
  if config_path is None:
    config_path = _config_path(dest)

  config = _load_config(config_path)
  before, after = config.get('before'), config.get('after')

  if before and hasattr(before, '__call__'):
    before(config)

  name = config.get('__template__')
  template_path = _template_path(name)
  _build_template(template_path, dest, config_path, overwrite)

  if after and hasattr(after, '__call__'):
    after(config)
