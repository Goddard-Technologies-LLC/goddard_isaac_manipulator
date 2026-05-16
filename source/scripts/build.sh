#!/bin/bash

# Builds the project workspaces

# Resolve the root directory
PROJECT_ROOT="$(pwd)"

# Isaac ROS
echo building Isaac ROS workspace...
cd ${ISAAC_ROS_WS}
colcon build --symlink-install --packages-up-to isaac_manipulator_pick_and_place --cmake-args "-DBUILD_TESTING=OFF"

# Goddard
echo building Goddard workspace...
cd /kiosk/source/workspaces/goddard # path root uses Docker bound volume name (see docker.sh)
colcon build --symlink-install --cmake-args "-DBUILD_TESTING=OFF"

# Universal Robots
echo building Universal Robots workspace...
cd /kiosk/source/workspaces/universal_robots
colcon build --symlink-install --cmake-args "-DBUILD_TESTING=OFF"

# Source all builds
cd ${PROJECT_ROOT}
source source/scripts/source.sh
