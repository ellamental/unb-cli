import os

from lib.commands.commands import arg, Group


group = Group(
  title='Create projects or directories from templates.',
  description='Create projects or directories from templates.',
)


@group.command(name='list')
def list_templates():
  """List available templates."""
  from unb_cli.templates import list_templates
  for t in list_templates():
    print t


@group.command(name='new')
@arg('name')
def new_template(name):
  """Create a new project template in ~/.unb-cli.d/templates/name."""
  from unb_cli.templates import new_template
  try:
    new_template(name)
  except OSError:
    print 'Error creating template.'


@group.command(name='cc')
@arg('name')
@arg('dest', nargs='?')
def copy_config(name, dest):
  """Copy the config from a template to the current directory or dest."""
  from unb_cli.templates import copy_config
  if not dest:
    dest = os.getcwd()
  copy_config(name, dest)


@group.command(name='build')
@arg('name')
def build_template(name):
  """Build a template from a config file (in the current directory)."""
  from unb_cli.templates import build_template
  build_template(name, os.getcwd())
# TODO(nick): Add an option to create a new UNB project config at
#   `~/.unb-cli.d/projects/name`.
