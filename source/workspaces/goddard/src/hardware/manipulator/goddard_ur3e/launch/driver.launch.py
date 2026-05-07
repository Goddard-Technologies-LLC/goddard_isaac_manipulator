# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


# FUNCTIONS
def declare_launch_args() -> list[DeclareLaunchArgument]:
    args: list[DeclareLaunchArgument] = []
    args.append(DeclareLaunchArgument(name="robot_ip", default_value="192.24.24.24"),)
    args.append(DeclareLaunchArgument(name="simulate", default_value="false"),)
    return args


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:

    # Initialize launch arguments
    robot_ip = LaunchConfiguration("robot_ip")
    simulate = LaunchConfiguration("simulate")

    # Defer to the UR vendor's own driver package
    ur_control = IncludeLaunchDescription(
        launch_description_source = PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("ur_robot_driver"),
                "launch",
                "ur_control.launch.py"
            ])
        ),
        launch_arguments = {
            "ur_type":              "ur3e",
            "description_package":  "goddard_ur3e",
            "description_file":     "ur.urdf.xacro",
            "use_fake_hardware":    simulate,
            "robot_ip":             robot_ip,
            "launch_rviz":          "false"
        }.items()
    )

    return LaunchDescription([*declare_launch_args(), ur_control])
