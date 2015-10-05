"""
UNB CLI
=======

The UNB Command Line Interface.

This project provides useful commands and utilities for creating and working
with UNB projects.

"""

import os
from setuptools import setup, find_packages


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE_PATH = os.path.join(PROJECT_DIR, 'VERSION')


# TODO(nick): Maybe find some way to have unb-cli include this.
def read_version():
  if not os.path.isfile(VERSION_FILE_PATH):
    raise EnvironmentError("Version file not found.")
  with open(VERSION_FILE_PATH) as f:
    return f.read().strip()


if __name__ == '__main__':
  setup(
    name='unb-cli',
    version=read_version(),
    description='Command line utilities for UNB project development.',
    author='Nick Zarczynski',
    author_email='nick@unb.services',
    url='https://bitbucket.org/unbsolutions/unb-cli',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'flake8',  # linting
      'jinja2',  # templating (project creation)
    ],
    scripts=[
      'unb_cli/scripts/unb.sh',
    ],
    entry_points='''
      [console_scripts]
      unb-cli=unb_cli.unb:cli
    ''',
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Console',
      'Framework :: Django :: 1.8',
      'License :: OSI Approved :: MIT License',
      'Operating System :: POSIX',
      'Programming Language :: Python :: 2.7',
    ],
  )
