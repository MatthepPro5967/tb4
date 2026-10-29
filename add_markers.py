#!/usr/bin/env python3
"""Put ArUco markers into the running sim (run ./run_sim.sh first).

  ./add_markers.py

Edit MARKERS below to change how many there are and where they go.
"""
import os
import subprocess

import cv2

# One line per marker: (marker id, x, y, yaw).
# The robot starts at (0, 0). After undocking it faces -x, so these signs
# stand 2.5 m in front of it, turned (yaw 0) to face it.
MARKERS = [
    (0, -2.5, -1.0, 0.0),
    (1, -2.5, 0.0, 0.0),
    (2, -2.5, 1.0, 0.0),
]

SIGN_SIZE = 0.4    # whole sign, including the white border (meters)
HEIGHT = 0.3       # height of the sign's center above the floor (meters)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'markers')
DICTIONARY = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

# A sign is a thin static box with the marker picture on it.
MODEL_SDF = """<?xml version="1.0"?>
<sdf version="1.9">
  <model name="aruco_{id}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry><box><size>0.01 {size} {size}</size></box></geometry>
        <!-- emissive_map makes the sign light itself up, so it shows even
             in worlds with no lights (like the warehouse). -->
        <material>
          <ambient>1 1 1 1</ambient>
          <diffuse>1 1 1 1</diffuse>
          <pbr><metal>
            <albedo_map>{image}</albedo_map>
            <emissive_map>{image}</emissive_map>
            <metalness>0</metalness>
          </metal></pbr>
        </material>
      </visual>
      <collision name="collision">
        <geometry><box><size>0.01 {size} {size}</size></box></geometry>
      </collision>
    </link>
  </model>
</sdf>
"""


def make_marker(marker_id):
    """Step 1 and 2: save the marker picture and the Gazebo model file for it."""
    # Step 1: OpenCV draws the black-and-white marker. The white border
    # (padding) is needed: the detector can't find a marker without it.
    image = cv2.aruco.drawMarker(DICTIONARY, marker_id, 300)
    image = cv2.copyMakeBorder(image, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
    image_path = os.path.join(OUT_DIR, f'aruco_{marker_id}.png')
    cv2.imwrite(image_path, image)

    # Step 2: the model file says "a thin square with this picture on it".
    sdf_path = os.path.join(OUT_DIR, f'aruco_{marker_id}.sdf')
    with open(sdf_path, 'w') as f:
        f.write(MODEL_SDF.format(id=marker_id, size=SIGN_SIZE, image=image_path))
    return sdf_path


def spawn(sdf_path, marker_id, x, y, yaw):
    """Step 3: ask the running sim to add the model at (x, y)."""
    result = subprocess.run([
        'ros2', 'run', 'ros_gz_sim', 'create',
        '-file', sdf_path, '-name', f'aruco_{marker_id}',
        '-x', str(x), '-y', str(y), '-z', str(HEIGHT), '-Y', str(yaw),
    ], capture_output=True, text=True)
    return 'successful' in result.stderr + result.stdout


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    for marker_id, x, y, yaw in MARKERS:
        if spawn(make_marker(marker_id), marker_id, x, y, yaw):
            print(f'Added marker {marker_id} at x={x}, y={y}')
        else:
            print(f'Marker {marker_id} not added (already there, or is the sim running?)')
