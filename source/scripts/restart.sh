#!/bin/bash

# Stops the Isaac ROS Docker container

echo stopping Docker container...

# Is the container running?
CONTAINER_NAME="isaac_ros_dev-x86_64-container"
if [ "$(docker inspect -f '{{.State.Running}}' ${CONTAINER_NAME} 2>/dev/null)" = "true" ]; then
    docker stop ${CONTAINER_NAME}
    echo container stopped successfully
else
    echo container is not running
fi
