#!/bin/bash

# Launches the Isaac ROS docker container

# Resolve this script's directory
SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Attach this project to the docker container as a bound volume ("kiosk")
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && ./scripts/run_dev.sh \
    -d ${ISAAC_ROS_WS} \
    --docker_arg "-v ${SCRIPT_DIRECTORY}:/kiosk" \
    --skip_image_build
