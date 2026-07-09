import rclpy

from .turtlebot3_pyqt_gui_node import Turtlebot3PyQtGuiNode
from ..signals.RosSignalsManager import SignalsManager

class RobotConnection():

    def __init__(self):

        self._node = None

        SignalsManager.ros_connect_requested.connect(self.connect)
        SignalsManager.ros_disconnect_requested.connect(self.disconnect)

    @property
    def node(self):
        return self._node

    @property
    def is_connected(self):
        return self._node is not None

    def connect(self):

        if self._node is not None:
            return

        self._node = Turtlebot3PyQtGuiNode()

        SignalsManager.emit_ros_node_connection_changed(True)

    def disconnect(self):

        if self._node is None:
            return

        self._node.destroy_node()
        self._node = None

        SignalsManager.emit_ros_node_connection_changed(False)

    def spin_once(self):

        if self._node is None:
            return

        rclpy.spin_once(self._node, timeout_sec=0)
