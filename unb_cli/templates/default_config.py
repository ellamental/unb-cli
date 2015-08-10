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
python_name = 'something_cool'
verbose_name = 'Something Cool'

project_description = 'A cool project description.  Can be long.'

version = '0.0.1'


# Additional Directories
# ======================


# Additional directories to create for this project.  All standard directories
# (that a tool like ``unb-cli`` would expect) are provided below.  However,
# since not every project will make use of them, only the common ones are
# uncommented.
#
# There's no need to let this tool create these directories.  You may create
# them manually as well.  Additionally, most tools (like ``unb-cli``) should be
# configurable for how your individual project is setup.
create_directories = [
  # Every project should have a sub-directory of the same name as the Python
  # package that represents the project.  The contents of this directory will
  # be shipped as the final product, either in source form, as package files
  # or some binary.  This is done to keep meta-information out of the end
  # user's package, which makes it smaller and more efficient to transfer and
  # store.
  #
  # There's very little reason to skip this directory, or name it something
  # other than the name of your Python package.  However, should you really
  # need to do this, you can configure it here.

  python_name,

  # Almost every project will have a docs directory.  Your project's
  # documentation goes here, whether you create that documentation by hand
  # (maybe as markdown files) or you utilize a tool like Sphinx.
  #
  # There may be additional directory structure that will be expected by
  # documentation tools.  Since this isn't standard, we won't add it.

  'docs',

  # Project-specific external libraries.  Maybe these have been forked, or are
  # just really small and should be included, or are in staging to be removed
  # from the app... Whatever the reason, lib is for them.
  #
  # Generally you will use your build tool to manage packaging this with your
  # app if necessary, though you could also simply move this directory into
  # your app directory.

  # 'lib',

  # Project scripts.  These could do anything.  They usually will act on the
  # project in some way (maybe even regularly via cron or something) but
  # they're not really a part of the app.  An example might be scripts to
  # reset a database, or perform other maintenence tasks.
  # Could also make a ``unb scripts script_name`` command that will run these
  # scripts...?

  # 'scripts',

  # Maybe this goes in scripts/build instead?
  # Scripts, utilities or assets needed to build the project.
  # The ``unb build`` command could accept these script names as an argument
  # and run them ``unb build script_name.sh``?

  # 'build',
]


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
