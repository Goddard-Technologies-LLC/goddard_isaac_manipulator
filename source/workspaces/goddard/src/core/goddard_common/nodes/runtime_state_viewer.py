#!/usr/bin/python3

# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( EXTERNAL )
import cv2

# IMPORTS ( ROS )
import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import String

# IMPORTS ( STANDARD )
from abc import ABC as Abstract
from abc import abstractmethod
from pathlib import Path
from typing import Type

# IMPORTS ( PACKAGE )
from api.nodes import NodeRunner
from api.runtime import RuntimeState


# CONSTANTS
RESOURCE_FOLDER: Path = Path(get_package_share_directory("goddard_common")) / "resources/images/runtime"
RUNTIME_STATE_IMAGES: dict[RuntimeState, Path] = {
    # RuntimeState.IDLE:      Path(IMAGE_FOLDER) / "state_idle.png",
    RuntimeState.NORMAL:    Path(RESOURCE_FOLDER) / "state_normal.png",
    RuntimeState.FAULT:     Path(RESOURCE_FOLDER) / "state_fault.png",
    RuntimeState.PAUSED:    Path(RESOURCE_FOLDER) / "state_paused.png",
    RuntimeState.CAUTION:   Path(RESOURCE_FOLDER) / "state_caution.png",
    # RuntimeState.WARNING:   Path(IMAGE_FOLDER) / "state_warning.png",
    RuntimeState.ERROR:     Path(RESOURCE_FOLDER) / "state_error.png",
    RuntimeState.COLLISION: Path(RESOURCE_FOLDER) / "state_collision.png",
    RuntimeState.NO_PATH:   Path(RESOURCE_FOLDER) / "state_no_path.png",
}


# CLASSES
class RenderService(Abstract):
    """Renders images to a graphical window."""

    # CLASS ATTRIBUTES
    tick_rate: int = 10 # Hz
    image = None
    
    # ABSTRACT METHODS
    @abstractmethod
    def render(self, image: Path):
        """Renders the target image to the window."""
        ...

    @abstractmethod
    def update(self):
        """Tick method (runs on every time step)."""
        ...


class CV2Graphics(RenderService):

    # INTRINSIC METHODS
    def __init__(self):
        super().__init__()
        self.window_title = "Runtime State"
        cv2.namedWindow(self.window_title, cv2.WINDOW_NORMAL)

    # INTRINSIC METHODS
    def __del__(self):
        cv2.destroyAllWindows()

        # ^ NOTE: probably not necessary, as the render service is likely running
        # for the entire lifespan of the ROS program anyways.

    # OVERRIDDEN METHODS
    def render(self, image):
        super().render(image)

        # Simply ingest the image and cache the result; the update() method will
        # handle the rendering on its next tick.

        processed = cv2.imread(str(image))
        if processed is not None:
            self.image = processed
    
    def update(self):
        super().update()
        if self.image is not None:
            cv2.imshow(self.window_title, self.image)
            cv2.waitKey(1) # process GUI events


class RuntimeStateViewer(Node):
    """Renders the current runtime state to a graphical window."""
    
    # INTRINIC METHODS
    def __init__(self, node_name: str, graphics: Type[RenderService], images: dict[RuntimeState, Path]):
        super().__init__(node_name)
        self.images = images

        # We need to tick the render loop manually
        self.get_logger().info(f"starting graphics service (tick rate: {graphics.tick_rate} Hz)")
        self.graphics = graphics()

        interval = 1.0 / graphics.tick_rate # convert Hz to period (seconds)
        self.tick = self.create_timer(interval, self.graphics.update)

        # Subscribe to state change topic
        self.subscription = self.create_subscription(
            msg_type    = String,
            topic       = "runtime_state_change",
            callback    = self.handle_state_change,
            qos_profile = 10
        )

        # Render default image
        self._render(self._lookup(RuntimeState.ERROR))

        # Log ready
        self.get_logger().info("listening for runtime state changes...")

    # PUBLIC METHODS
    def handle_state_change(self, message: String):
        """Adapts the inbound ROS message for use with the low-level render operation."""
        self.get_logger().info(f"received state change: {message.data}")

        # Is the new state valid (a member of the state enum)?
        try:
            state = RuntimeState[message.data]
        except KeyError:
            self.get_logger().warning(f"cannot process unrecognized runtime state: {message.data}")
            return
        
        # Do we have a corresponding image for the state?
        if not (image := self._lookup(state)):
            self.get_logger().warning(f"failed to get image for state: {state}")
            return
        
        # Render the image
        self.get_logger().info(f"rendering image for state: {state}")
        self._render(image)

    # PRIVATE METHODS
    def _render(self, image: Path):
        """Delegates the atomic rendering operation to the render service."""
        try:
            self.graphics.render(image)
        except Exception as error:
            self.get_logger().error(f"failed to render state image: {str(image)}")
            self.get_logger().error(error)

    def _lookup(self, state: RuntimeState) -> Path:
        """Retrieves an image resource using a runtime state."""
        return self.images.get(state)


# ENTRY POINT
if __name__ == "__main__":
    rclpy.init()
    node = RuntimeStateViewer("runtime_state_viewer", CV2Graphics, RUNTIME_STATE_IMAGES)
    NodeRunner.execute(node)
