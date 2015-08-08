import os
import shutil
import subprocess

from lib.commands.commands import arg, Group

from unb_cli.create_project import template

from . import config


group = Group(
  title='Create projects and apps from templates.',
  description='Create projects and apps from templates.',
)


@group.command(name='new-py')
def new_py():
  config_path = os.path.join(os.getcwd(), 'config.py')
  template.copy_config('project_template', config_path)
  loader = template.get_loader('project_template',
                               config_path=config_path,
                               out_path=os.getcwd())
  loader.render_project()


@group.command(name='py-project')
@arg('config_path')
def py_project(config_path):
  """Create a standard Python project."""
  loader = template.get_loader('project_template')
  loader.render_project(overwrite=False)


@group.command(name='config')
def create_config_file():
  """Copy an existing config to get started."""
  dest = os.path.join(os.getcwd(), 'config.py')
  template.copy_config('project_template', dest)
