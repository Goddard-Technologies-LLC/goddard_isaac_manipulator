#!/bin/bash

# Sources all of the project overlays

# List of workspaces
WORKSPACES=(
    "goddard"
    "nvidia"
    "universal_robots"
)

echo "sourcing project overlays..."

# Source each workspace overlay
for workspace in "${WORKSPACES[@]}"; do
    setup_file="source/workspaces/${workspace}/install/setup.bash"

    if [ -f "$setup_file" ]; then
        source "$setup_file"
    else
        echo "warning: $setup_file not found"
    fi
done
