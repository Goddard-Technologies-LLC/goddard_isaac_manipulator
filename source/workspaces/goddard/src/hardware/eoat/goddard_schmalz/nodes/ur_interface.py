# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( ROS )
from ur_msgs.srv import SetIO

# IMPORTS ( STANDARD )
from dataclasses import dataclass
from typing import TYPE_CHECKING

# IMPORTS ( PACKAGE )
from interface import SchmalzControlInterface

if TYPE_CHECKING:
    from controller import SchmalzController


# CLASSES
class URInterface(SchmalzControlInterface):
    
    # INTRINSIC METHODS
    def __init__(self, controller):
        super().__init__(controller)

        # Define a service & corresponding client
        self.io_service = controller.declare_parameter("ur_gripper_service", "/io_and_status_controller/set_io")
        self.io_client = controller.create_client(SetIO, self.io_service.get_parameter_value().string_value)

    # OVERRIDDEN METHODS
    def connect(self, timeout):
        super().connect(timeout)
        return self.io_client.wait_for_service(timeout_sec=timeout)

    def activate(self):
        super().activate()
        try:
            self._set_io(SetIO.Request.PIN_TOOL_DOUT0, SetIO.Request.STATE_OFF)
            self._set_io(SetIO.Request.PIN_TOOL_DOUT1, SetIO.Request.STATE_ON)
            return True
        except Exception as error:
            self.controller.get_logger().warning(f"failed to set IO states: {error}")
            return False
    
    def deactivate(self):
        super().deactivate()
        try:
            self._set_io(SetIO.Request.PIN_TOOL_DOUT0, SetIO.Request.STATE_ON)
            self._set_io(SetIO.Request.PIN_TOOL_DOUT1, SetIO.Request.STATE_OFF)
            return True
        except Exception as error:
            self.controller.get_logger().warning(f"failed to set IO states: {error}")
            return False
    
    # PRIVATE METHODS
    def _set_io(self, pin: int, state: int):
        message         = SetIO.Request()
        message.fun     = SetIO.Request.FUN_SET_DIGITAL_OUT
        message.pin     = pin
        message.state   = float(state)
        self.io_client.call_async(message)
