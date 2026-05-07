# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# TODO: In the future, this should get brought into the Isaac ROS ecosystem to leverage
# CuMotion as a motion planning option.


# IMPORTS ( ROS )
from launch import LaunchDescription, LaunchContext, Action
from launch.actions import OpaqueFunction, DeclareLaunchArgument, IncludeLaunchDescription
# from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
    actions: list[Action] = []

    # Initialize launch arguments
    simulate    = context.launch_configurations["simulate"]
    robot_ip    = context.launch_configurations["robot_ip"]
    manip       = context.launch_configurations["manip"]
    eoat        = context.launch_configurations["eoat"]

    # Defer to the target manipulator's demo launch
    manip_controller = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare(f"goddard_{manip}"),
                "launch",
                "demo.launch.py"
            ])
        ),
        launch_arguments = {
            "robot_ip": robot_ip,
            "simulate": simulate
        }.items()
    )

    # Start the target eoat's controller node
    if eoat != "none":
        eoat_controller = Node(
            # condition   = IfCondition(using_eoat),
            package     = [
                TextSubstitution(text='goddard_'),
                eoat
            ],
            executable  = "controller.py",
            parameters  = [{"interface": manip}],
            output      = "screen",
        )
        actions.append(eoat_controller)

        # TODO: ^ Replace if statement with conditional launch substitution
    
    return [manip_controller, *actions]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        *declare_launch_args(),
        OpaqueFunction(function=launch_setup)
    ])
