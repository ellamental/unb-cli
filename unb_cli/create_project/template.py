# import pdb; pdb.set_trace()

import os
import logging
import shutil

import jinja2


logger = logging.getLogger(__name__)
logging.basicConfig()


PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))


# Not sure what to do with this yet.. We should really construct the project
# auto-magically given a configuration file.

def _get_loader(project_name):
  path = os.path.join(PACKAGE_PATH, project_name, 'templates')
  return jinja2.Environment(
    loader=jinja2.FileSystemLoader(path),
    keep_trailing_newline=True,
    autoescape=False,
  )


def _project_path(project_name):
  return os.path.join(PACKAGE_PATH, project_name)


def _templates_path(project_name):
  return os.path.join(_project_path(project_name), 'templates')


def _get_config_path(project_name):
  return os.path.join(_project_path(project_name), 'config.py')


def _load_config(path, env=None):
  if env is None:
    ret = {}
  else:
    ret = dict(env)
  execfile(path, ret)
  del ret['__builtins__']
  return ret

def copy_config(project_name, dest):
  config_path = _get_config_path(project_name)
  if not os.path.exists(dest):
    shutil.copy(config_path, dest)


# Default Template Library
# ========================

import markup
from library import wrap, wrap_block, pystr

default_env = {
  'markup': markup,
  'wrap': wrap,
  'wrap_block': wrap_block,
  'pystr': pystr,
}


# Template Rendering
# ==================


class Templates(object):
  def __init__(self, project_name, config_path=None, out_path=None):
    self.loader = _get_loader(project_name)
    self.templates_path = _templates_path(project_name)

    self.config_path = config_path
    if config_path is None:
      self.config_path = _get_config_path(project_name)

    self.config = _load_config(self.config_path)

    self.default_env = default_env
    self.default_env = dict(default_env, **self.config)

    self.out_path = out_path
    if out_path is None:
      self.out_path = os.path.join(_project_path(project_name), 'out')

  def render(self, template_path, context=None):
    env = self.default_env
    if context is not None:
      env = dict(env, **context)
    return self.loader.get_template(template_path).render(env)

  def render_to_file(self, template_path, output_full_path, context=None,
                     overwrite=False, create_dirs=True):
    content = self.render(template_path, context)
    if create_dirs:
      if not os.path.exists(os.path.dirname(output_full_path)):
        os.makedirs(os.path.dirname(output_full_path))
    if os.path.exists(output_full_path):
      if overwrite != True:
        logger.info('Did not render.  File exists at: %s',
                    os.path.basename(output_full_path))
        return
      else:
        logger.warn('Overwriting file: %s', os.path.basename(output_full_path))
    with open(output_full_path, 'w') as f:
      f.write(content)

  def renderf(self, template_path, context=None, overwrite=False):
    out_full_path = os.path.join(self.out_path, template_path)
    self.render_to_file(template_path, out_full_path, context, overwrite)

  def _render_all_templates_to_file(self, extra_context=None, overwrite=False):
    file_paths = os.listdir(self.templates_path)
    for file_path in file_paths:
      self.render_to_file(file_path, extra_context, overwrite)

  def _render_license(self, license):
    """Render the LICENSE file based on the chosen license type.

    Each type of license will have its own template.  This method will choose
    the correct template, render it with the config values and write it to
    the LICENSE file.
    """
    pass

  def _make_dir(self, dirname):
    dir_path = os.path.join(self.out_path, dirname)
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

  def _make_dirs(self, dirnames=None):
    if dirnames is None:
      dirnames = self.config.get('create_directories')
    if dirnames:
      for dirname in dirnames:
        self._make_dir(dirname)

  def render_project(self, extra_context=None):
    file_paths = os.listdir(self.templates_path)
    rerenderable = self.config.get('rerenderable', [])
    for file_path in file_paths:
      if file_path in rerenderable:
        self.renderf(file_path, extra_context, overwrite=True)
      else:
        self.renderf(file_path, extra_context, overwrite=False)
    self._make_dirs()


# get_loader
# ==========


def get_loader(project_name, config_path=None, out_path=None):
  return Templates(project_name, config_path, out_path)


"""
import template

loader = template.get_loader('project_template')

loader.render_project(overwrite=False)

"""
