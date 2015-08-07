# -*- coding: utf-8 -*-
"""
Default configuration for a Django project.

You are encouraged to import this into your config file and override values and
settings as you need.
"""

# I'm not sure what to do with the files/directories thing.  Really it's just
# a placeholder for now.
files = [
  'README.rst',

  # Populated from config value.
  'VERSION',

  # This should just be copied in from a directory of standard licenses, based
  # on a config value.  Hmmm... each license might need to be customized (even
  # if only with a standard template).
  'LICENSE',

  # Standard requirements for Django, also allow optional packages..
  'requirements.txt',

  # Simple, standard
  '.gitignore',

  # Even for non-packages.
  'setup.py',

  # the below are not necessary for many projects

  # Additional requirements it only makes sense to install on dev machines.
  # There could also be test-requirements to be done on testing servers or
  # something... I'm not sure.
  'dev-requirements.txt',

  # Project-specific setup of 3rd party code (like flake8).
  'setup.cfg',

  # Creating a Heroku project should generate a fair bit of things (like
  # adding the heroku cli to the system deps (whereever we decide to store
  # information like that).
]

directories = [
  # This will be populated with the Sphinx docs, or markdown, or whatever.
  'docs',

  # project_name (config var = python_name)
  'project_name',

  # the below may or may not be necessary

  # Project-specific external libraries.  Maybe these have been forked, or are
  # just really small and should be included, or are in staging to be removed
  # from the app... Whatever the reason, lib is for them.
  'lib',

  # Project scripts.  These could do anything.  They usually will act on the
  # project in some way (maybe even regularly via cron or something) but
  # they're not really a part of the app.  An example might be scripts to
  # reset a database, or perform other maintenence tasks.
  # Could also make a ``unb scripts script_name`` command that will run these
  # scripts...?
  'scripts',

  # Maybe this goes in scripts/build instead?
  # Scripts, utilities or assets needed to build the project.
  # The ``unb build`` command could accept these script names as an argument
  # and run them ``unb build script_name.sh``?
  'build',
]


project_name = 'unb-cli'  # lowercase variant
python_name = 'unb_cli'
capitalized_name = 'UNB CLI'

is_heroku = True
heroku_app_name = 'unbcli'
