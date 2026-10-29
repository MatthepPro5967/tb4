#!/bin/bash
# One-time install of ROS 2 Jazzy + Gazebo Harmonic + TurtleBot4 dependencies.
# Run with:  ./install_deps.sh   (it will ask for your sudo password)
set -e

# 1. Add the ROS 2 apt repository
sudo apt update
sudo apt install -y curl software-properties-common
sudo add-apt-repository -y universe
ROS_APT_VER=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F tag_name | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_VER}/ros2-apt-source_${ROS_APT_VER}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

# 2. Install ROS 2 Jazzy, build tools, and Gazebo Harmonic
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools git

# 3. Install everything the TurtleBot4 simulator source in src/ depends on
source /opt/ros/jazzy/setup.bash
[ -f /etc/ros/rosdep/sources.list.d/20-default.list ] || sudo rosdep init
rosdep update
rosdep install --from-paths "$(dirname "$0")/src" --ignore-src -y

echo "Done. Next: ./build.sh"
