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

    # Launch the runtime state viewer
    runtime_viewer = Node(
        package     = "goddard_common",
        executable  = "runtime_state_viewer.py",
        output      = "screen"
    )

    # TODO: Launch an intermediate listener node that adapts and relays Isaac
    # pose-to-pose states to the runtime state viewer

    # Start the manipulator's driver
    manip_driver = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare(f"goddard_{manip}"),
                "launch",
                "driver.launch.py"
            ])
        ),
        launch_arguments = {
            "robot_ip": robot_ip,
            "simulate": simulate,
            "launch_rviz": "false"
        }.items()
    )

    # Start CuMotion-enabled MoveIt
    moveit = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("isaac_ros_cumotion_examples"),
                "launch",
                "ur.launch.py"
            ])
        ),
        launch_arguments = {
            "ur_type":  manip,
            "robot_ip": robot_ip,
            "simulate": simulate,
            "launch_rviz": "false",
            "description_package": f"goddard_{manip}",
            "description_file": "ur.urdf.xacro",
            "moveit_config_package": f"goddard_{manip}",
            "moveit_config_file": "ur.srdf.xacro",
        }.items()
    )

    # Start the Isaac ROS pose-to-pose workflow
    pose_to_pose = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("isaac_manipulator_bringup"),
                "launch",
                "cumotion_nvblox_pose_to_pose.launch.py"
            ])
        ),
        launch_arguments = {
            "camera_type": "realsense",
            "num_cameras": "1",
            "setup": "goddard_kiosk",
            "robot_file_name": PathJoinSubstitution([
                FindPackageShare("goddard_pose_to_pose"), "xrdf", f"{manip}_{eoat}.xrdf"
            ]),
            "urdf_file_path": PathJoinSubstitution([
                FindPackageShare("goddard_pose_to_pose"), "urdf", f"{manip}_{eoat}.urdf",
            ]),
        }.items()
    )

    # return [runtime_viewer, manip_driver, moveit, pose_to_pose]
    return [manip_driver, moveit, pose_to_pose]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        *declare_launch_args(),
        OpaqueFunction(function=launch_setup)
    ])
