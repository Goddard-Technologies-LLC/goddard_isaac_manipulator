#!/usr/bin/python3

# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# Send triggers with the following service calls:
#   - ros2 service call <activation_topic> std_srvs/srv/Trigger {}
#   - ros2 service call <deactivation_topic> std_srvs/srv/Trigger {}


# IMPORTS ( ROS )
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

# IMPORTS ( STANDARD )
from typing import Type

# IMPORTS ( PACKAGE )
from interface import SchmalzControlInterface
from ur_interface import URInterface


# CONSTANTS
SUPPORTED_INTERFACES: dict[str, SchmalzControlInterface] = {
    "ur3e": URInterface,
    "ur5e": URInterface
}


# CLASSES
class SchmalzController(Node):
    """A simple controller that listens for activate/deactivate triggers."""
    
    # INTRINSIC METHODS
    def __init__(self, node_name: str):
        super().__init__(node_name)

        # Expose & resolve the interface type argument
        try:
            self.declare_parameter("interface", "ur3e")
            interface = self._resolve_interface("interface")
        except KeyError as error:
            self.get_logger().error(error)
            return
        
        # Define & connect to the platform-specific interface
        self.interface = interface(self)
        self._connect(self.interface, timeout=1.0, retries=10)

        # Define ROS services
        self.activation_service = self.create_service(Trigger, "/gripper/activate", self.activate)
        self.deactivation_service = self.create_service(Trigger, "/gripper/deactivate", self.deactivate)
        
    # PUBLIC METHODS
    def activate(self, request: Trigger.Request, response: Trigger.Response):
        """Activates the gripper vacuum."""
        self._log_request(self.activate.__name__)
        if self.interface.activate():
            response.success = True
            response.message = "gripper vacuum activated"
        else:
            response.success = False
            response.message = "gripper vacuum activation failed"
        self.get_logger().info(response.message)
        return response

    def deactivate(self, request: Trigger.Request, response: Trigger.Response):
        """Deactivates the gripper vacuum."""
        self._log_request(self.deactivate.__name__)
        if self.interface.deactivate():
            response.success = True
            response.message = "gripper vacuum deactivated"
        else:
            response.success = False
            response.message = "gripper vacuum deactivation failed"
        self.get_logger().info(response.message)
        return response
    
    def _connect(self, interface: SchmalzControlInterface, timeout: float = 3.0, retries: int = 3):
        """Connects to the platform-specific control interface."""
        self.get_logger().info(f"connecting to {self.get_parameter('interface').value} gripper service...")

        attempts: int = 1
        while (attempts <= retries) and not interface.connect(timeout):
            self.get_logger().warning(f"gripper service not available (attempt {attempts}/{retries})")
            attempts += 1

        if attempts > retries:
            self.get_logger().error("maximum connection attempts reached")
            raise TimeoutError
        
        self.get_logger().info("successfully connected to gripper service!")

    # PRIVATE METHODS
    def _log_request(self, function_name: str):
        self.get_logger().info(f"received gripper control request: {function_name}")

    def _resolve_interface(self, param: str) -> Type[SchmalzControlInterface]:
        arg = self.get_parameter(param).value
        if not (interface := SUPPORTED_INTERFACES.get(arg, None)):
            raise KeyError(f"gripper interface type not supported: {arg}")
        return interface


# ENTRY POINT
if __name__ == "__main__":
    rclpy.init()
    node = SchmalzController("schmalz_controller")
    rclpy.spin(node)
    rclpy.shutdown()
