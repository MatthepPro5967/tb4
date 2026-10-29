#!/bin/bash
# Add the AR markers to the running sim, then open the marker detector.
# Run after ./run_sim.sh. Ctrl+C closes the detector.
cd "$(dirname "$0")"
# The VS Code snap terminal changes these, which crashes the camera window.
unset GTK_PATH GTK_EXE_PREFIX GIO_MODULE_DIR GTK_IM_MODULE_FILE LOCPATH GSETTINGS_SCHEMA_DIR
# VS Code saves the real value of each setting it changed as NAME_VSCODE_SNAP_ORIG.
# Put every one of them back.
for saved in $(compgen -v | grep '_VSCODE_SNAP_ORIG$'); do
  name=${saved%_VSCODE_SNAP_ORIG}
  if [ -n "${!saved}" ]; then export "$name=${!saved}"; else unset "$name"; fi
done
source /opt/ros/jazzy/setup.bash
python3 add_markers.py
python3 detect_markers.py
