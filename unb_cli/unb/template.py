import os

from clams import arg, Command


template = Command(
  name='template',
  title='Create projects or directories from templates.',
  description='Create projects or directories from templates.',
)


@template.register('list')
def list_templates():
  """List available templates."""
  from unb_cli.templates import list_templates
  for t in list_templates():
    print t


@template.register('new-template')
@arg('name')
def new_template(name):
  """Create a new project template in ~/.unb-cli.d/templates/name."""
  from unb_cli.templates import new_template
  try:
    new_template(name)
  except OSError:
    print 'Error creating template.'


@template.register('new')
@arg('template_name')
@arg('dirname')
def new_template(template_name, dirname):
  """Copy the configuration file for `template_name` to dirname.

  To see a list of available template names use `unb template list`.

  If dirname does not exist, it will be created.

  """
  from unb_cli.templates import copy_config
  if not os.path.exists(dirname):
    os.mkdir(dirname)
  os.chdir(dirname)
  copy_config(template_name, os.getcwd())
  print
  print '=========='
  print 'Next steps'
  print '=========='
  print
  print 'cd ' + dirname
  print 'emacs __config__.py'
  print 'unb template build  # ut build'


@template.register('cc')
@arg('name')
@arg('dest', nargs='?')
def copy_config(name, dest):
  """Copy the config from a template to the current directory or dest."""
  from unb_cli.templates import copy_config
  if not dest:
    dest = os.getcwd()
  copy_config(name, dest)


@template.register('build')
def build_template():
  """Build a template from a config file (in the current directory)."""
  from unb_cli.templates import build_template
  build_template(os.getcwd())
# TODO(nick): Add an option to create a new UNB project config at
#   `~/.unb-cli.d/projects/name`.
