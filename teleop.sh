#!/bin/bash
# Drive the TurtleBot4 with the keyboard (run while the sim is running).
# Keys: i = forward, , = back, j/l = turn, k = stop. Click this terminal first.
source /opt/ros/jazzy/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
