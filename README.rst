####################################
UNB Command Line Interface (unb-cli)
####################################


.. WARNING::  This package is in the process of being converted for public
              use.  There will be some rough edges.

`unb-cli` is a suite of tools created to standardize common project management
tasks for **UNB packages and applications**.

`unb-cli` is available semi-publicly for the convenience of developers
contributing to UNB packages.  This package should be considered "unreleased"
and absolutely no promises are made to keep backward compatibility in any way.



Installation
============

Install from the shell with:

.. code-block:: shell

   pip install --user unb-cli --extra-index-url https://pypi.fury.io/nickfrez/


Or add the following to your ``requirements.txt``:

.. code-block:: text

   --extra-index-url https://gemfury.com/nickfrez
   unb-cli==0.0.12


Or for dev install, clone the repo and use:

.. code-block:: shell

    pip install -e /path/to/unb-cli/


Depending on your configuration and how you install `unb-cli` you may need to
add something like the following to your shell startup scripts
(``.bash-profile``, ``.bashrc``, etc.):

.. code-block:: bash

   if [[ $OSTYPE == linux* ]]; then
       # Linux
       export PATH="$HOME/.local/bin:$PATH"
       source $HOME/.local/bin/unb.sh

   elif [[ $OSTYPE == darwin* ]]; then
       # OS X
       export PATH="/usr/local/bin:$PATH"
       source /usr/local/bin/unb.sh

   else
       # Unknown
       echo "OS Unknown.  Did not source unb command."
   fi

Sourcing the ``unb.sh`` script makes the ``unb`` command available.  The
``unb`` command is a lightweight bash function that wraps the ``unb-cli``
command to allow ``unb`` to modify the current shell session (for things like
activating Python virtual environments).

Examples throughout this project and its documentation will assume that you use
the ``unb`` function, instead of calling ``unb-cli`` directly.


Configuration
-------------

``unb-cli`` project support can be configured through ``~/.unb-cli.d/``.  This
aspect of ``unb-cli`` is sorely under-documented.


Projects
~~~~~~~~

Many UNB CLI commands operate on/in a project.  A "project" is generally
defined as a git repo.  The "current project" is the repository stored at the
first parent directory of ``$PWD`` that contains a ``.git`` directory.

Projects may be configured by a project configuration Python script located at
``~/.unb-cli.d/projects/project-name.py``.

For more documentation see:

.. code-block:: console

   $ unb project -h


Templates
~~~~~~~~~

.. code-block:: console

   $ unb template -h


Templates provide a convenient method of creating new projects, directories
and/or files that conform to a standardized layout.  Templates are powered by
`jinja2 <http://jinja.pocoo.org/docs/dev/>`_.

Templates are (currently) assumed to be stored at
``~/.unb-cli.d/templates/*``.  At some point in the near future, a separate
project will be released containing the standard templates used for UNB
projects.  Until that point, the template system is going to remain largely
undocumented.



Example
=======

.. code-block:: console

   $ unb
   usage: unb-cli [-h]
                  {b,dj,docs,gemfury,heroku,lint,node,pip,project,shell,template,version}
                  ...
   unb-cli: error: too few arguments


.. code-block:: console

   $ unb -h
   usage: unb-cli [-h]
                  {b,dj,docs,gemfury,heroku,lint,node,pip,project,shell,template,version}
                  ...

   positional arguments:
     {b,dj,docs,gemfury,heroku,lint,node,pip,project,shell,template,version}
       b                   Execute functions contained in a project's
                           project_root/build.py file.
       dj                  Django commands and tasks.
       docs                Documentation tools.
       gemfury             Gemfury package management tools
       heroku              Heroku project/environment management tools
       lint                Run linters.
       node                node.js tools
       pip                 pip interface and tools
       project             Project management utilities
       shell               Run a Python shell.
       template            Create projects or directories from templates.
       version             Utilities for versioning and releases.

   optional arguments:
     -h, --help            show this help message and exit



Documentation
=============

Currently `unb-cli` is documented primarily through the `-h` option available
in the shell.

.. code-block:: console

   $ unb -h


Each subcommand also has ``-h`` and ``--help`` options.



Issue Reporting and Contact Information
=======================================

If you have any problems with this software, please take a moment to report
them by email to nick@unb.services.

If you are a security researcher or believe you have found a security
vulnerability in this software, please contact us by email at
nick@unb.services.



Contributing
============

Contributions are always welcome, whether it's reporting a bug or sending a
pull request.  If you want to help, but don't know where to start, email me at
nick@unb.services and I'll try to point you in the right direction.



Copyright and License Information
=================================

Copyright (c) 2015 Nick Zarczynski

This project is licensed under the MIT license.  Please see the LICENSE file
for more information.
