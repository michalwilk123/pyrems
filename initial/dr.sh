drawer() {
    if [ "$1" = "list" ] || [ "$1" = "add" ]; then
        python3 /home/user/path/to/pyrems/drawer.py "$@"
    else
        local cmd=$(python3 /home/user/path/to/pyrems/drawer.py "$@")
        if [ $? -eq 0 ] && [ -n "$cmd" ]; then
            history -s "$cmd"
            echo "$cmd"
            # This puts it in history and displays it
            # Then use: !! to recall it for editing
        fi
    fi
}
