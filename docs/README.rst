Copyright (c) Goddard Technologies, Inc. All rights reserved.


GAR006-Kiosk-Controller
=======================

Control framework for the Goddard demo kiosk (GAR006).

Provides discrete modules for composing perception-driven robotic arm tasks. Contains pose-to-pose and pick-and-place programs with dynamic obstacle avoidance powered by Isaac ROS cuMotion.


Installation
============

This project relies on `git submodules <https://www.atlassian.com/git/tutorials/git-submodule>`__ to grab a snapshot of vendor repositories. Use the following command to ensure that all of the included submodules *(and their own submodules)* are installed locally:

.. code-block:: bash

    git clone --recurse-submodules https://github.com/Goddard-Technologies-LLC/GAR006-Kiosk-Controller

This project also uses `git subtrees <https://www.atlassian.com/git/tutorials/git-subtree>`__ as a means of forking vendor repositories. Updates to any subtrees need to be pushed to their respective repos - an example local git setup is shown below:

.. code-block:: bash

    kiosk-user@kioskPC:~/GAR006-KioskController$ git remote -v
    isaac_manipulator       https://github.com/Goddard-Technologies-LLC/goddard_isaac_manipulator (fetch)
    isaac_manipulator       https://github.com/Goddard-Technologies-LLC/goddard_isaac_manipulator (push)
    origin  https://github.com/Goddard-Technologies-LLC/GAR006-Kiosk-Controller (fetch)
    origin  https://github.com/Goddard-Technologies-LLC/GAR006-Kiosk-Controller (push)

Once the project is installed, source ``setup.sh`` in the project's root directory. This will configure the project environment and generate default configuration data. This action only needs to happen once; running the script again is not harmful, but it will reset any configured parameters to their default values.

ROS2 Humble
-----------
This project is built with **ROS2 Humble**. Refer to the `online documentation <https://docs.ros.org/en/humble/Installation.html>`__ to perform your ROS installation. It is highly recommended to `add sourcing <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html#add-sourcing-to-your-shell-startup-script>`__ to your shell startup script to enable access to your ROS environment from any terminal.


Isaac ROS
---------
The core workflows in this project rely on **Isaac ROS (release-3.2)**. Refer to the `online documentation <https://nvidia-isaac-ros.github.io/v/release-3.2/getting_started/index.html#setup>`__ to prepare your Isaac ROS environment. Replace step 4 of the environment configuration procedure with the commands below [#f]_:

.. code-block:: bash

    mkdir -p  ~/workspaces/isaac_ros-dev/src
    echo "export ISAAC_ROS_WS=${HOME}/GAR006-Kiosk-Controller/source/workspaces/nvidia" >> ~/.bashrc
    source ~/.bashrc

Support for RealSense cameras requires a rebuild of the Docker container.

- **DO NOT** clone the ``isaac_ros_common`` repo in step 1; this is already included in the project.

- **DO** skip straight to step 4. *This will take 10-15 minutes:*

.. code-block:: bash

    cd ${ISAAC_ROS_WS}/src/isaac_ros_common && \
    ./scripts/run_dev.sh -d ${ISAAC_ROS_WS}


Quickstart
==========

1 - Build
---------
You must enter the Isaac ROS Docker container (via ``docker.sh``) prior to running any build processes. This ensures that the build system leverages the context provided by the Docker environment.

- Once you are inside the container, call ``cd /kiosk-controller`` to navigate to the project root.

The project must be rebuilt any time changes are made to the source code:

- The ``compile.sh`` script can be sourced to rebuild the entire project. *This will take 5-10 minutes for a new project installation.*

- The ``build.sh`` script exposes a function for building individual workspaces. This can significantly reduce total build time by targetting only specific parts of the codebase that have been modified. See the example usage below:

.. code-block:: bash

    source source/scripts/build.sh
    build universal_robots # build only this workspace

- Standard ROS2 ``colcon_build`` commands can be also used in place of any of the provided build scripts.

2 - Configure
-------------
Configurable parameters can be found in ``config.local.yaml``. These parameters propagate to all workflow packages via the top-level launch package ``goddard_launch``. For a list of acceptable values for each parameter, refer to ``constraints.yaml`` contained therein.

3 - Launch
----------
To run a configured program, simply navigate to the projct root and execute ``launch.sh``. Standard ROS2 ``ros2 launch`` and ``ros2 run`` commands can also be used to run individual package launchers & nodes *(this bypasses the goddard_launch package, therefore configured parameters will not be applied automatically)*.


Project Structure
=================

Workspaces
----------
The project is divided into discrete ROS workspaces. Workspaces are categorized by vendor to keep dependencies clear and simple. Most workflows expect that all workspaces are built and sourced.

Packages
--------
A package is the smallest logical unit of compartmentalized functionality. By default, all packages are c-style (`ament_cmake <https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html>`__), regardless of their linguistic composition. This approach helps to standardize and unify package development. Packages with Python code should be configured to use ament_python as an additional build dependency in ``CMakeLists.txt`` and ``package.xml``. 

Resources
---------
The ``resources`` folder is a bucket for contextual/development data:

- Base assets from which project assets are derived (CAD models, Blender files, etc.)
- IDE configuration templates
- etc.

Nothing contained within this folder should be runtime critical; if removing it would alter the program in any way, **it doesn't belong here**.


Footnotes
=========
.. [#f] If you choose to clone this repository anywhere other than the Home directory, you must update the ${ISAAC_ROS_WS} path accordingly.