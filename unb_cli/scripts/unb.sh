
# To get the UNB command you will need to add this to your .bash_profile
#
#     source $HOME/.local/bin/unb.sh


function unb-deactivate-virtualenv () {
    # If a virtualenv is already active, deactivate it.
    if hash deactivate 2>/dev/null; then
        deactivate
    fi
}


function unb () {
    # Wrapper for the unb-cli Python utility.

    if ! hash unb 2>/dev/null; then
        echo "error: unb-cli must be installed."
        return 1
    fi

    # unb-cli install-requirements
    # unb-cli clear-cache

    if [ "$1" == "go" ]; then
        if [ -z "$2" ]; then
            project_name="unb-platform"
            projectpath="$(unb-cli project path unb-platform)"
        else
            project_name=$2
            projectpath="$(unb-cli project path $project_name)"
        fi

        cd $projectpath

        # Should check if we need to (de)activate.
        unb-deactivate-virtualenv
        activate_path="$(unb-cli project venv-activate-path $project_name)"
        source $activate_path
        echo "Go go go!"
    else
        # Delegate to the python unb-cli
        unb-cli "$@"
    fi
}
