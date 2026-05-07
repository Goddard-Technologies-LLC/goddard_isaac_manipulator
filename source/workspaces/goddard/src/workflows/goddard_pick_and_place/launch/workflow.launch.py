# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# NOTE: Due to limitations imposed by the Isaac ROS xrdf format, this workflow
# currently only supports pre-compiled manipulator/eoat combinations.

# TODO: Separate out the URDF when complete manip/eoat modularity is implemented.
# This package shouldn't have to maintain any urdfs.


# IMPORTS ( ROS )
from launch import LaunchDescription, LaunchContext, Action
from launch.actions import DeclareLaunchArgument, OpaqueFunction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.logging import get_logger
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


# FUNCTIONS
def declare_launch_args() -> list[DeclareLaunchArgument]:
    args: list[DeclareLaunchArgument] = []
    args.append(DeclareLaunchArgument(name="simulate"),)
    args.append(DeclareLaunchArgument(name="robot_ip"),)
    args.append(DeclareLaunchArgument(name="manip"),)
    args.append(DeclareLaunchArgument(name="eoat"),)
    return args


def launch_setup(context: LaunchContext, *args, **kwargs) -> list[Action]:

    # Initialize launch arguments
    simulate    = context.launch_configurations["simulate"]
    robot_ip    = context.launch_configurations["robot_ip"]
    manip       = context.launch_configurations["manip"]
    eoat        = context.launch_configurations["eoat"]

    # Start the Isaac ROS pick-and-place workflow
    pick_and_place = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("isaac_manipulator_pick_and_place"),
                "launch",
                "ur_pick_and_place.launch.py"
            ])
        ),
        launch_arguments = {
            "robot_ip": robot_ip,
            "ur_type": manip,
            "gripper_type": "robotiq_2f_140",
            "setup": "goddard_kiosk",
            "camera_type": "realsense",
            "num_cameras": "1",
            "use_pose_from_rviz": "true",
            "object_attachment_type": "cuboid",
            "object_attachment_scale": "0.10",
        }.items()
    )

    return [pick_and_place]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        *declare_launch_args(),
        OpaqueFunction(function=launch_setup)
    ])
