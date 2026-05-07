Errors
======

The ``_get_version()`` function in ``source/workspaces/nvidia/src/isaac_ros_cumotion/curobo_core/curobo/src/curobo/__init__.py`` needs to be replaced with the following:

.. code-block:: python

    def _get_version():
    """Return the version string used for __version__."""
    return "v0.7.0-no-tag"


NVIDIA's instructions for pick and place w/ the ros2_robotiq_gripper package are bogus. Run the following inside the docker container
to grab the necessary build dependencies:

.. code-block:: bash
    source /opt/ros/humble/setup.bash
    rosdep update
    rosdep install -i -r --from-paths ${ISAAC_ROS_WS}/src/ros2_robotiq_gripper --rosdistro humble -y


You need to accept the EULA for isaac_ros_peoplenet_models_install...

.. code-block:: bash
    ERROR: Please run the following command to view and accept the EULA before downloading "rsu_rs_480_640_mask":
    /workspaces/isaac_ros-dev/src/isaac_ros_object_detection/isaac_ros_peoplenet_models_install/asset_scripts/install_peoplenet_amr_rs.sh --eula
    or set environment variable: ISAAC_ROS_ACCEPT_EULA=1
