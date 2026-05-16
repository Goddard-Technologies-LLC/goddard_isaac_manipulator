#!/bin/bash

# Initializes the project

echo "Initializing project..."

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

# Download NVIDIA assets
source source/scripts/assets.sh

echo "setup complete!"
