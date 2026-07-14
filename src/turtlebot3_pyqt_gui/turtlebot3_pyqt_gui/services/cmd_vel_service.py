import rclpy
from geometry_msgs.msg import Twist
from ..ros.ros_manager import IROSManager


class CmdVelService:
    def __init__(self, ros: IROSManager):
        self._ros = ros

        self._publisher = None
        self._init_publisher()

    def _init_publisher(self):
        if self._ros.gui_node is None:
            return
        self._publisher = self._ros.gui_node.create_publisher(Twist, '/cmd_vel', 10)

    def send_command(self, command, linear, angular):
        if self._publisher is None:
            self._init_publisher()

        if self._publisher is None:
            return

        msg = Twist()
        if command == 'stop':
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        elif command == 'forward':
            msg.linear.x = linear
            msg.angular.z = 0.0
        elif command == 'backward':
            msg.linear.x = -linear
            msg.angular.z = 0.0
        elif command == 'left':
            msg.linear.x = 0.0
            msg.angular.z = angular
        elif command == 'right':
            msg.linear.x = 0.0
            msg.angular.z = -angular
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self._publisher.publish(msg)
