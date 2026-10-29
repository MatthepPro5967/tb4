#!/bin/bash
# Launch Gazebo with a TurtleBot4 in the warehouse world.
# Add rviz:=true to also open RViz (it tends to crash on Ctrl+C, which is harmless).
# Extra args are passed through, e.g.  ./run_sim.sh world:=maze model:=lite
cd "$(dirname "$0")"
# The VS Code snap terminal sets these, which crashes Gazebo's GUI and RViz.
unset GTK_PATH GTK_EXE_PREFIX GIO_MODULE_DIR GTK_IM_MODULE_FILE LOCPATH GSETTINGS_SCHEMA_DIR
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py rviz:=false "$@"
