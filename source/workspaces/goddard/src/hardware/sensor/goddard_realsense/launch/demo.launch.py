# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
from launch import LaunchDescription, LaunchContext, Action
from launch.actions import OpaqueFunction
from launch_ros.actions import Node


# FUNCTIONS
def launch_setup(context: LaunchContext, *args, **kwargs) -> list[Action]:
    return [
        Node(
            package     = "goddard_realsense",
            executable  = "viewer.py",
            output      = "screen",
    )]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])
