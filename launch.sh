#!/bin/bash

# Launches the top-level ROS package

# Ensure the ROS underlay is sourced
source /opt/ros/${ROS_DISTRO}/install/setup.sh

# Ensure all of the project overlays are sourced
source ./source/scripts/source.sh

# Run top-level launch file
ros2 launch goddard_launch kiosk.launch.py
