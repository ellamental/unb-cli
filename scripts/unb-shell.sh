
# Error if UNB_PROJECT_DIR is not set.
# TODO(nick): Make this actually work... Bash could use some modernization.
# ${UNB_PROJECT_DIR:?Error "\$UNB_PROJECT_DIR must be set to point to UNB git root."}

# Management commands/utilities directories
UNB_MANAGEMENT_DIR=$UNB_PROJECT_DIR/management
UNB_SCRIPTS=$UNB_MANAGEMENT_DIR/scripts

# Virtual environment directory/scripts
UNB_VENV_DIR=$UNB_PROJECT_DIR/venv
UNB_VENV_ACTIVATE=$UNB_VENV_DIR/bin/activate


function unb-activate-virtualenv () {
    echo "Activating virtual environment..."
    # If a virtualenv is already active, deactivate it.
    if hash deactivate 2>/dev/null; then
        deactivate
    fi
    source $UNB_VENV_ACTIVATE
}


function unb-go () {
    # Go to the UNB project, activate the virtual environment and maybe more!

    cd $UNB_PROJECT_DIR

    unb-activate-virtualenv

    # If the ``unb`` command is installed, do some more stuff...
    if hash unb 2>/dev/null; then
        unb install-requirements
        unb clear-cache
    fi
}



# Unb Setup
# ---------

# TODO(nick): This should be the bare-minimum to install the ``unb`` management
#   command, then have the ``unb`` command take over from there.

function unb-create-virtualenv () {
    if [ ! -d $UNB_VENV_DIR ]; then
        echo "Creating virtual environment..."
        virtualenv venv
    fi
}


function unb-install-unb () {
    cd $UNB_MANAGEMENT_DIR
    pip install --editable .
    cd $UNB_PROJECT_DIR
}


function unb-setup-postgres () {
    createdb unb
    echo "create user unb password 'unb'" | psql
}


function unb-setup () {
    # TODO(nick): This doesn't play well with other apps.
    echo "Add the following to your .bash_profile or .bashrc:"
    echo "export DJANGO_SETTINGS_MODULE=unb.settings.dev"

    # TODO(nick): Every command needs to be idempotent.
    unb-create-virtualenv
    unb-install-unb
    unb install-requirements
    unb-setup-postgres
    unb m migrate
    # TODO(nick): Automate this?
    # unb m createsuperuser
}
