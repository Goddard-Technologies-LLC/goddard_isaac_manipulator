#!/bin/bash

# Attach this project to the docker container as a bound volume ("kiosk-controller")
cd ${ISAAC_ROS_WS}/src/isaac_ros_common && ./scripts/run_dev.sh \
    -d ${ISAAC_ROS_WS} \
    --docker_arg "-v ${HOME}/GAR006-Sandbox/sandbox-03:/kiosk-controller" \
    --skip_image_build
