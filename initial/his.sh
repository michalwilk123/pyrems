#!/bin/bash

# Display the last used command
history | tail -2 | head -1 | sed 's/^[ ]*[0-9]*[ ]*//' | xargs echo
