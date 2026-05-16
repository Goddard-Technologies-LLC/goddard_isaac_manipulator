#!/bin/bash

# Exposes a reusable build function

build() {

    # Check if at least one workspace
    if [ "$#" -lt 1 ]; then
        paint "$ORANGE" "Usage: build_dirs <dir1> <dir2> ..."
        return 1
    fi

    # Loop over all workspaces
    BASE_DIR="${PWD}/source/workspaces"
    for dir in "$@"; do
        WORKSPACE_DIR="$BASE_DIR/$dir"
        if [ -d "$WORKSPACE_DIR" ]; then
            echo "\nBuilding workspace: $dir"
            cd "$WORKSPACE_DIR" || { paint "$RED" "Failed to enter $WORKSPACE_DIR"; continue; }
            rm -r build log
            colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF
            cd - > /dev/null  # Return to the original directory
        else
            echo "ERROR: workspace directory not found: $WORKSPACE_DIR"
        fi
    done
}
