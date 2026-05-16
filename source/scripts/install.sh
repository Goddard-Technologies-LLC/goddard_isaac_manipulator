#!/bin/bash

# Installs the project dependencies

echo installing project dependencies...

cd ${ISAAC_ROS_WS}

# Get latest apt data
sudo apt-get update

# Install Python dependencies
pip install swiftserialize

# Get latest ROS data
rosdep update

# Accept EULA for any Isaac ROS dependencies
export ISAAC_ROS_ACCEPT_EULA=1

# BUGFIX: robotiq dependency issue
rosdep install -i -r \
    --from-paths ${ISAAC_ROS_WS}/src/ros2_robotiq_gripper \
    --rosdistro humble -y

colcon build --symlink-install --packages-select-regex robotiq* serial --cmake-args "-DBUILD_TESTING=OFF" && \
source install/setup.bash

# Install & build Isaac ROS dependencies
rosdep install -i -r \
    --from-paths ${ISAAC_ROS_WS}/src/isaac_manipulator/isaac_manipulator_pick_and_place/ \
    --rosdistro humble -y
