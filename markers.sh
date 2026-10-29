#!/bin/bash
# Add the AR markers to the running sim, then open the marker detector.
# Run after ./run_sim.sh. Ctrl+C closes the detector.
cd "$(dirname "$0")"
# The VS Code snap terminal sets these, which crashes the camera window.
unset GTK_PATH GTK_EXE_PREFIX GIO_MODULE_DIR GTK_IM_MODULE_FILE LOCPATH GSETTINGS_SCHEMA_DIR
source /opt/ros/jazzy/setup.bash
python3 add_markers.py
python3 detect_markers.py
