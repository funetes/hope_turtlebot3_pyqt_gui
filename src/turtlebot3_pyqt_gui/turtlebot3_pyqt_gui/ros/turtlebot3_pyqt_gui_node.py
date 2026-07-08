import rclpy
from rclpy.node import Node


class Turtlebot3PyQtGuiNode(Node):
    def __init__(self):
        super().__init__("turtlebot3_pyqt_gui")
        self._timer = self.create_timer(0.01, self._spin_once)


    def _spin_once(self):
        rclpy.spin_once(self, timeout_sec=0)
