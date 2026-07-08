import rclpy
from rclpy.node import Node

from signals.RosSignalsManager import SignalsManager
from sensor_msgs.msg import BatteryState


class Turtlebot3PyQtGuiNode(Node):
    def __init__(self):
        super().__init__("turtlebot3_pyqt_gui")
        self._timer = self.create_timer(0.01, self._spin_once)

        self.signalsManager = SignalsManager

        self.battery_sub = self.create_subscription(
            BatteryState, "/battery_state", self.battery_state_callback, 10
        )

    def battery_state_callback(self, msg: BatteryState):
        self.signalsManager.battery_status_received.emit(msg)

    def _spin_once(self):
        rclpy.spin_once(self, timeout_sec=0)
