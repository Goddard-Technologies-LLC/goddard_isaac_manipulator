#!/bin/bash

# SCRIPT DEPENDENCIES
source ./source/scripts/colors.sh
source ./source/scripts/build.sh

# Accept EULA for any Isaac ROS dependencies
export ISAAC_ROS_ACCEPT_EULA=1

# Get latest data
sudo apt-get update

# Install Python dependencies
pip install swiftserialize

# Install & build Isaac ROS's own rosdep dependencies
rosdep update && \
   rosdep install -i -r \
   --from-paths ${ISAAC_ROS_WS}/src/isaac_manipulator/isaac_manipulator_pick_and_place/ \
   --rosdistro humble -y

# Build Isaac ROS workspace
cd ${ISAAC_ROS_WS}
colcon build --symlink-install --packages-up-to isaac_manipulator_pick_and_place
source install/setup.bash

# Navigate to project root
cd /kiosk-controller

# Build standard workspaces
build goddard universal_robots

# Source all workspaces
source source/scripts/source.sh
