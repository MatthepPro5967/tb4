#!/usr/bin/env python3
"""Watch the robot's camera and find ArUco markers (run while the sim is running).

  ./detect_markers.py

Opens a window with the camera view, draws a box around each marker it sees,
and prints the marker's id and how far away it is.
"""
import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image

# Size of the black square only, not the white border (meters).
# add_markers.py makes 0.4 m signs, and the black part is 3/4 of that.
MARKER_SIZE = 0.3

DICTIONARY = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

# What to call each marker id. Add a line here for each new marker.
NAMES = {
    0: 'apple',
    1: 'banana',
    2: 'orange',
}


class MarkerDetector(Node):
    def __init__(self):
        super().__init__('marker_detector')
        self.bridge = CvBridge()
        self.camera_matrix = None
        self.seen = set()  # markers that were in view last frame
        self.got_frame = False
        self.create_subscription(CameraInfo, '/oakd/rgb/preview/camera_info', self.on_info, 10)
        self.create_subscription(Image, '/oakd/rgb/preview/image_raw', self.on_image, 10)

    def on_info(self, msg):
        # The camera's lens settings, needed to work out distance.
        self.camera_matrix = np.array(msg.k).reshape(3, 3)
        self.distortion = np.array(msg.d)

    def on_image(self, msg):
        if not self.got_frame:
            self.got_frame = True
            print('Camera connected. Point the robot at a marker.', flush=True)
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # OpenCV finds the markers: their corners and their ids.
        corners, ids, _ = cv2.aruco.detectMarkers(gray, DICTIONARY)

        in_view = set()
        if ids is not None and self.camera_matrix is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            # From the corners, the known marker size, and the lens
            # settings, OpenCV works out where the marker is.
            _, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, MARKER_SIZE, self.camera_matrix, self.distortion)
            for marker_id, tvec in zip(ids.flatten(), tvecs):
                in_view.add(marker_id)
                # Only print when a marker first comes into view, not every frame.
                if marker_id not in self.seen:
                    name = NAMES.get(marker_id, f'marker {marker_id}')
                    distance = np.linalg.norm(tvec)
                    print(f'I see {name}! ({distance:.2f} m away)', flush=True)
        self.seen = in_view

        # Show it 2x bigger, since the sim camera is only 320x240.
        cv2.imshow('Markers', cv2.resize(frame, None, fx=2, fy=2))
        cv2.waitKey(1)


def main():
    rclpy.init()
    print('Waiting for the camera... (Ctrl+C to stop)', flush=True)
    rclpy.spin(MarkerDetector())


if __name__ == '__main__':
    main()
