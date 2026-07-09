import rclpy

from .turtlebot3_pyqt_gui_node import Turtlebot3PyQtGuiNode
from ..signals.RosSignalsManager import SignalsManager
from PyQt5.QtCore import QObject, pyqtSlot

class RobotConnection(QObject):

    def __init__(self):
        super().__init__()

        self._node = None

        SignalsManager.ros_connect_requested.connect(self.node_connect)
        SignalsManager.ros_disconnect_requested.connect(self.node_disconnect)

    @property
    def node(self):
        return self._node

    @property
    def is_connected(self):
        return self._node is not None

    @pyqtSlot()
    def node_connect(self):

        print("connect:", id(self), self._node)

        if self._node is not None:
            print("already connected")
            return

        self._node = Turtlebot3PyQtGuiNode()
        print("created:", id(self._node))

        SignalsManager.emit_ros_node_connection_changed(True)

    @pyqtSlot()
    def node_disconnect(self):

        if self._node is None:
            return

        self._node.destroy_node()
        self._node = None

        SignalsManager.emit_ros_node_connection_changed(False)

    def spin_once(self):

        if self._node is None:
            return

        rclpy.spin_once(self._node, timeout_sec=0)
