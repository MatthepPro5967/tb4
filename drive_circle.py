#!/usr/bin/env python3
"""Minimal example: drive the TurtleBot4 in a circle.

Run in a second terminal while the sim is running:
    source /opt/ros/jazzy/setup.bash && source install/setup.bash
    python3 drive_circle.py
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class DriveCircle(Node):
    def __init__(self):
        super().__init__('drive_circle')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_timer(0.1, self.tick)  # 10 Hz

    def tick(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = 0.2   # m/s forward
        msg.twist.angular.z = 0.4  # rad/s turning
        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(DriveCircle())


if __name__ == '__main__':
    main()
