#!/bin/bash

# Attach this project to the docker container as a bound volume ("kiosk-controller")
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && ./scripts/run_dev.sh \
    --docker_arg "-v ${HOME}/GAR006-Kiosk-Controller:/kiosk-controller"
    --docker_arg "-b/--skip_image_build"
