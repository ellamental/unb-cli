"""
Shell Scripts
=============

The UNB project contains a number of shell scripts intended to make common
tasks during development a bit less painful.

Primarily they are used as a bootstraping mechanism to launch the UNB
project and activate the virtual environment, after which the ``unb``
management command is intended to take over.


Installation
------------

The shell scripts are "installed" by sourcing the script file in your
``.bashrc`` or other appropriate location.

There are 3 main components.

- UNB_PROJECT_DIR: used by other scripts to determine project location
- unb-go: cd to the project directory and activate the virtual environment
- unb: contains many management sub-commands to simplify and standardize common
  tasks.

Simply open ``~/.bashrc`` in your favorite editor and add the following lines.
You'll need to set ``UNB_DIR`` to point to your specific installation of the
UNB project files.

::

   # UNB repos and other files
   export UNB_DIR=/media/data/dev/unb

   # UNB_PROJECT_DIR must be set to the root directory of the UNB git repo!!!
   export UNB_PROJECT_DIR=$UNB_DIR/unb-platform

   # Other convenient paths
   export UNB_SCRIPTS=$UNB_PROJECT_DIR/management/scripts

   # unb-go (cd to project directory, create+activate virtualenv, etc.)
   source $UNB_SCRIPTS/unb-shell.sh

   # unb command auto-completion (only available in Bash)
   source $UNB_SCRIPTS/unb-complete.sh


unb-go
------

``unb-go`` is a shell script that launches and activates the UNB project
within your shell.

Simply use ``unb-go`` anywhere, anytime, and you will be transported to the
UNB project with the virtual environment created+activated and
dependencies installed.

"""
