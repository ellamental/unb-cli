"""
Gemfury Utilities
=================

Gemfury package management tools.

"""

import argparse
import subprocess

from clams import arg, Command


command = Command(
  name='gemfury',
  title='Gemfury package management tools',
  description='Gemfury package management tools',
)


@command.register(name='add-remote')
@arg('username', help="Gemfury username to publish this package to.")
@arg('package_name', help="Name to publish the package as.")
def add_remote(username, package_name):
  """Add a Gemfury git remote `fury` to the current git repo."""
  url = 'https://git.fury.io/' + username + '/' + package_name + '.git'
  subprocess.call(['git', 'remote', 'add', 'fury', url])
  print
  print 'To push this package to Gemfury, use:'
  print
  print '    git push fury master'
  print
