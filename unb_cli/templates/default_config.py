# -*- coding: utf-8 -*-
"""
Default configuration for a Python project.

You are encouraged to import this into your config file and override values and
settings as you need.
"""

from datetime import datetime


# ==================================================================


# **WARNING** Any file here will get overwritten! **WARNING**
#
# These files should NEVER be hand-edited.
#
# Any file not listed here will never be re-rendered.
#
# Why would you ever re-generate your project anyway?  You may want to update
# your project to use newer versions of the standard project layout.
rerenderable = [
  'setup.py',
  'LICENSE',
]


# ==================================================================


# General Project Information
# ===========================

project_name = 'something-cool'
app_name = 'something_cool'
verbose_name = 'Something Cool'

project_description = 'A cool project description.  Can be long.'

version = '0.0.1'


# Author Information
# ==================

author = 'Nick Zarczynski'
author_email = 'nick@unb.services'


# Links
# =====

# The main url:  A general url that could apply to any audience.
project_url = 'git@bitbucket.org:unbsolutions/something-cool.git'

# Specific urls
public_url = 'git@bitbucket.org:unbsolutions/something-cool.git'
source_url = 'git@bitbucket.org:unbsolutions/something-cool.git'
# docs_url = Found in the Documentation section.
# issue_tracker = Found in the Issue Tracking section.


# License Information
# ===================

def copyright_years(start, end):
  start = str(start)
  end = str(end)
  if start == end:
    return end
  else:
    return start + '-' + end

license = 'MIT'

copyright_start_year = datetime.today().year
copyright_end_year = datetime.today().year
copyright_holders = [
  author,
]

mit_copyright_line = ' '.join([
  'Copyright (c)',
  copyright_years(copyright_start_year, copyright_end_year),
  ', '.join(copyright_holders),
])


# Issue Tracking and Contact Information
# ======================================

issue_tracker_url = 'git@bitbucket.org:unbsolutions/something-cool.git'
issue_contact_email = author_email

# URL to direct people that contains information on how to report security
# vulnerabilities found in this software.
#
# Note that it's a very good idea to have this prominently displayed (such as
# in the footer of your site).  You want to make it easy for people to report
# and get acknowledgement of that report, so they don't post it on Twitter!
#
# Lookup "security vulnerability report" to get an idea of how most companies
# handle this.
security_reporting_url = None
security_reporting_email = author_email


primary_mailing_list_address = 'foo'
primary_mailing_list_subscription_url = None


# Documentation
# =============

documentation_url = None


# Virtual Environment
# ===================

# If your virtual environment directory is stored in the project itself, this
# will add it to the .gitignore.  Setting it to `None` will not write anything
# to the .gitignore.
venv_dir = 'venv'


# Classifiers commonly used in UNB projects
# For a full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [

  # 'Development Status :: 1 - Planning',
  'Development Status :: 2 - Pre-Alpha',
  # 'Development Status :: 3 - Alpha',
  # 'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  # 'Development Status :: 6 - Mature',
  # 'Development Status :: 7 - Inactive',

  # 'Environment :: Console',
  # 'Environment :: MacOS X',
  'Environment :: Web Environment',
  # 'Environment :: Web Environment :: Mozilla',
  # 'Environment :: X11 Applications',
  # 'Environment :: X11 Applications :: Gnome',
  # 'Environment :: X11 Applications :: GTK',
  # 'Environment :: X11 Applications :: KDE',
  # 'Environment :: X11 Applications :: Qt',

  'Framework :: Django',
  'Framework :: Django :: 1.8',
  # 'Framework :: Flask',
  # 'Framework :: IPython',
  # 'Framework :: Sphinx',

  # 'Intended Audience :: Developers',
  # 'Intended Audience :: End Users/Desktop',

  'License :: OSI Approved :: MIT License',
  # 'License :: Other/Proprietary License',

  'Natural Language :: English',

  # 'Operating System :: Android',
  # 'Operating System :: iOS',
  # 'Operating System :: MacOS :: MacOS X',
  # 'Operating System :: OS Independent',
  'Operating System :: POSIX :: Linux',

  'Programming Language :: Python',
  'Programming Language :: Python :: 2.7',
  # 'Programming Language :: Python :: 2 :: Only',
  # 'Programming Language :: Python :: 3',
  'Programming Language :: JavaScript',
  # 'Programming Language :: Unix Shell',

  # 'Topic :: Documentation :: Sphinx',
  # 'Topic :: Internet',
  # 'Topic :: Internet :: WWW/HTTP :: WSGI',
  'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
  # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
  # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
  # 'Topic :: Software Development :: Build Tools',
  # 'Topic :: Software Development :: Code Generators',
  # 'Topic :: Software Development :: Documentation',
  # 'Topic :: Software Development :: Libraries',
  # 'Topic :: Software Development :: Libraries :: Application Frameworks',
  # 'Topic :: Software Development :: Libraries :: Python Modules',
  # 'Topic :: Software Development :: Testing',
  # 'Topic :: Software Development :: User Interfaces',
  # 'Topic :: Software Development :: Version Control',
  # 'Topic :: System :: Installation/Setup',
  # 'Topic :: Text Editors :: Emacs',
  # 'Topic :: Text Processing :: Markup',
  # 'Topic :: Utilities',
]
