#!/bin/bash


# Python Dependencies
pip install swiftserialize

# Source overlays
source source/workspaces/goddard/install/setup.bash
source source/workspaces/nvidia/install/setup.bash
# source source/workspaces/universal_robots/install/setup.bash

# Run top-level launch file
ros2 launch goddard_launch goddard.launch.py
