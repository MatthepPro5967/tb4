#!/bin/bash
# Build the workspace (the TurtleBot4 simulator source in src/).
set -e
cd "$(dirname "$0")"
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
