# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
import rclpy
from rclpy.node import Node


# CLASSES
class NodeRunner:
    """Ultra-thin Node wrapper for simplified execution syntax."""

    # PUBLIC METHODS
    @staticmethod
    def execute(node: Node):
        """( BLOCKING ) starts an instance of the target node."""
        try:
            # node.get_logger().info(f"starting node: {node.get_name()}")
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.destroy_node()
