import os
import jinja2

optional_files = [
]

optional_dirs = [
  'lib',
  'scripts',
]

heroku_files = [
  'Procfile',
]

# Config file

def h1(val):
  return '=' * len(val)

def h2(val):
  return '-' * len(val)

def h3(val):
  return '~'


project_name = 'unb-cli'
verbose_name = 'UNB CLI'

requirements = [

]

dev_requirements = [

]

