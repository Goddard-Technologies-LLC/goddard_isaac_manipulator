#!/bin/bash

# SCRIPT DEPENDENCIES
source ./source/scripts/colors.sh

# Source workspace overlays
paint "$BLUE" "sourcing project overlays..."
source source/workspaces/goddard/install/setup.bash
source source/workspaces/nvidia/install/setup.bash
source source/workspaces/universal_robots/install/setup.bash
echo "done!"
