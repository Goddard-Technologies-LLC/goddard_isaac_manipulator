#!/bin/bash

# Launches the top-level ROS package

# BUG: Packages that depend on curobo will encounter a setuptools_scm versioning
# issue as a result of our submodule setup. There is a pathing issue, where .gitmodules
# paths work with our local environment, but not once we've entered the Docker
# container. SCM supports forced versioning - we're just declaring the appropriate
# version (see source/workspaces/nvidia/src/isaac_ros_cumotion/curobo_core/curobo/src/curobo/__init__.py)

export SETUPTOOLS_SCM_PRETEND_VERSION=0.7.5

# Ensure the ROS underlay is sourced
source /opt/ros/${ROS_DISTRO}/setup.sh

# Ensure all of the project overlays are sourced
source ./source/scripts/source.sh

# Run top-level launch file
ros2 launch goddard_launch kiosk.launch.py
