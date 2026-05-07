# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
from launch import LaunchDescription, LaunchContext, Action
from launch.actions import OpaqueFunction, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


# FUNCTIONS
def declare_launch_args() -> list[DeclareLaunchArgument]:
    args: list[DeclareLaunchArgument] = []
    args.append(DeclareLaunchArgument(name="simulate", default_value="false"),)
    args.append(DeclareLaunchArgument(name="robot_ip", default_value="192.24.24.24"),)
    args.append(DeclareLaunchArgument(name="manip", default_value="ur3e"),)
    return args


def launch_setup(context: LaunchContext, *args, **kwargs) -> list[Action]:
    
    # Initialize launch arguments
    simulate    = context.launch_configurations["simulate"]
    robot_ip    = context.launch_configurations["robot_ip"]
    manip       = context.launch_configurations["manip"]
    
    # Defer to the target manipulator's demo launch
    manip_driver = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare(f"goddard_{manip}"),
                "launch",
                "demo.launch.py"
            ])
        ),
        launch_arguments = {
            "robot_ip": robot_ip,
            "simulate": simulate,
            "output": "screen"
        }.items()
    )

    # Instantiate the gripper controller node
    schmalz_controller = Node(
        package     = "goddard_schmalz",
        executable  = "controller.py",
        parameters  = [{"interface": manip}],
        output      = "screen",
        # prefix      = 'gnome-terminal -- bash -c'
        # NOTE ^ This prefix is swallowing ROS args; needs to change
    )

    return [manip_driver, schmalz_controller]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        *declare_launch_args(),
        OpaqueFunction(function=launch_setup)
    ])
