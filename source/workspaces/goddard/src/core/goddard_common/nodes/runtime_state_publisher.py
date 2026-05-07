#!/usr/bin/python3
# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# IMPORTS ( STANDARD )
import random

# IMPORTS ( PACKAGE )
from api.runtime import RuntimeState


# CLASSES
class StatePublisher(Node):

    # INTRINSIC METHODS
    def __init__(self, node_name, interval: float = 1.0):
        super().__init__(node_name)
        self.get_logger().info("starting test publisher")
        self.publisher = self.create_publisher(
            msg_type    = String,
            topic       = "runtime_state_change",
            qos_profile = 10
        )
        self.timer = self.create_timer(interval, self.dispatch)

    def dispatch(self):
        message = String()
        message.data = random.choice(RuntimeState._member_names_)
        self.get_logger().info(f"publishing runtime state: {message.data}")
        self.publisher.publish(message)


# ENTRY POINT
if __name__ == "__main__":
    rclpy.init()
    node = StatePublisher("test_publisher", interval=.75)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        # rclpy.shutdown() this is already handled by ros on a keyboard interrupt
