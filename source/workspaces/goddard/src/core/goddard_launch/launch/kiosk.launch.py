# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
from launch import LaunchDescription, LaunchContext, Action
from launch.actions import OpaqueFunction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.logging import logging, get_logger
from launch_ros.substitutions import FindPackageShare

# IMPORTS ( STANDARD )
import os

# IMPORTS ( PACKAGE )
from src.launch import LaunchDefinition
from src.params import *


# LOGGING
log: logging.Logger = get_logger('launch')


# FUNCTIONS
def construct_definintion() -> LaunchDefinition:
    """Builds the top-level launch definition from configured launch
    parameters."""
    try:
        return LaunchDefinition(
            robot_ip    = RobotIPParameter(),
            manipulator = ManipTypeParameter(),
            eoat        = EoATTypeParameter(),
            workflow    = WorkflowParameter(),
            simulate    = SimulateParameter()
        )
    except ValueError as error:
        log.warning(error)
        log.warning("Is the failed argument registered in constraints.yaml?")
        return


def launch_setup(context: LaunchContext, *args, **kwargs) -> list[Action]:
    
    # Construct launch definition
    log.info("constructing launch definition")
    if not (definition := construct_definintion()):
        log.error("failed to construct launch definition")
        return
    log.info("successfully constructed launch definition")
    
    # Find the workflow package
    log.info("locating workflow package")
    workflow    = f"goddard_{definition.workflow.argument}"
    package     = FindPackageShare(workflow).find(workflow)
    launcher    = os.path.join(package, "launch", "workflow.launch.py")
    log.info(f"found package: {workflow}")

    # Launch workflow sub-launcher
    return [
        IncludeLaunchDescription(
            launch_description_source = PythonLaunchDescriptionSource(launcher),
            launch_arguments = {
                "simulate": str(definition.simulate.argument),
                "robot_ip": definition.robot_ip.argument,
                "manip":    definition.manipulator.argument,
                "eoat":     definition.eoat.argument,
            }.items()
        )
    ]


# ENTRY POINT
def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([OpaqueFunction(function=launch_setup)])
