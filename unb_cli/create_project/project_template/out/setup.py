"""
Something Cool
==============

A cool project description.  Can be long.

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
    name='something-cool',
    version=read_version(),
    description='A cool project description.  Can be long.',
    author='Nick Zarczynski',
    author_email='nick@unb.services',
    url='git@bitbucket.org:unbsolutions/something-cool.git',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Web Environment',
      'Framework :: Django',
      'Framework :: Django :: 1.8',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: JavaScript',
      'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
  )
