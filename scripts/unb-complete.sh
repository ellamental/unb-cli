_unb_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _UNB_COMPLETE=complete $1 ) )
    return 0
}

complete -F _unb_completion -o default unb;
