#!/bin/bash

# SCRIPT DEPENDENCIES
source ./source/scripts/colors.sh
source ./source/scripts/build.sh

paint "$BLUE" "Running initial project setup"

# Instantiate local config
echo "generating local config"
CONFIG_DEFAULT="config/config.default.yaml"
CONFIG_LOCAL="config/config.local.yaml"
cp ${CONFIG_DEFAULT} ${CONFIG_LOCAL}

# Add docker config for realsense
echo "generating docker config"
isaac_config_path=${ISAAC_ROS_WS}/src/isaac_ros_common/scripts/.isaac_ros_common-config
touch ${isaac_config_path}
echo CONFIG_IMAGE_KEY=ros2_humble.realsense > ${isaac_config_path}

# Prelim build
build goddard universal_robots
