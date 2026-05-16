#!/bin/bash

# Installs project dependencies

echo installing project dependencies...

# Get latest apt data
sudo apt-get update

# Install Python dependencies
pip install -r source/requirements.txt

# Ensure the ROS underlay is sourced
source /opt/ros/${ROS_DISTRO}/setup.bash

# Get latest ROS data
rosdep update

# Accept EULA for any Isaac ROS dependencies
export ISAAC_ROS_ACCEPT_EULA=1

# BUGFIX: robotiq dependency issue
rosdep install -i -r \
    --from-paths ${ISAAC_ROS_WS}/src/ros2_robotiq_gripper \
    --rosdistro ${ROS_DISTRO} -y

# Install & build Isaac ROS dependencies
rosdep install -i -r \
    --from-paths ${ISAAC_ROS_WS}/src/isaac_manipulator/isaac_manipulator_pick_and_place/ \
    --rosdistro ${ROS_DISTRO} -y
