#!/usr/bin/python3

# Copyright (c) Goddard Technologies, Inc. All rights reserved.


# IMPORTS ( EXTERNAL )
import cv2
import numpy as np
from nvblox_torch.datasets.realsense_dataset import RealsenseDataloader

# IMPORTS ( ROS )
import rclpy
from rclpy.node import Node

# IMPORTS ( STANDARD )
import time


# CLASSES
class CameraViewer(Node):
    """A simple viewer for rendering a Realsense camera stream to a viewport."""

    # INTRINSIC METHODS
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.window_title = "Camera Viewer"
        
        # Connect & render indefinitely
        self.camera = self._connect(interval=1.0, retries=10)
        while True:
            data = self.camera.get_data()
            self.render(data)

    # PUBLIC METHODS
    def render(self, data):

        # Extract raw data fields
        raw_rgb = data["raw_rgb"]
        raw_depth = data["raw_depth"]

        # Apply color to depth data
        depth = cv2.applyColorMap(cv2.convertScaleAbs(raw_depth, alpha=100), cv2.COLORMAP_JET)

        # Render to viewport
        images = np.hstack((raw_rgb, depth))
        cv2.namedWindow(self.window_title, cv2.WINDOW_NORMAL)
        cv2.imshow(self.window_title, images)
        cv2.waitKey(1) # process GUI events

    # PRIVATE METHODS
    def _connect(self, interval: float = 3.0, retries: int = 3) -> RealsenseDataloader:
        self.get_logger().info("connecting to Realsense camera...")
        attempts: int = 1
        while attempts <= retries:
            try:
                camera = RealsenseDataloader(clipping_distance_m = 3.0)
                self.get_logger().info("successfully connected to camera!")
                return camera
            except RuntimeError as error:
                # NOTE: ^ The data loader will error out if a camera is not connected
                self.get_logger().warning(f"device not available (attempt {attempts}/{retries})")
                time.sleep(interval)
                attempts += 1
        self.get_logger().error("maximum connection attempts reached")
        raise TimeoutError


# ENTRY POINT
if __name__ == "__main__":
    rclpy.init()
    node = CameraViewer("camera_viewer")
    rclpy.spin(node)
    rclpy.shutdown()
