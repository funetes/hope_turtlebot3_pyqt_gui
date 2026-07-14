from typing import Protocol

import rclpy

from rclpy.executors import MultiThreadedExecutor
from ..signals.RosSignalsManager import SignalsManager
from .turtlebot3_pyqt_gui_node import Turtlebot3PyQtGuiNode

from PyQt5.QtCore import QObject


class IROSManager(Protocol):

    @property
    def gui_node(self) -> Turtlebot3PyQtGuiNode:
        ...

    @property
    def is_connected(self) -> bool:
        ...

    def connect(self):
        ...

    def disconnect(self):
        ...

    def spin_once(self):
        ...

    # def send_cmd_vel(self, linear: float, angular: float):
    #     ...

    # def get_robot_pose(self):
    #     ...

    # def get_battery(self):
    #     ...

class ROSManager(QObject):
    def __init__(self):
        super().__init__()

        self._executor = None

        self._gui_node = None

        self._nodes = []

        self._connected = False

    @property
    def gui_node(self):
        return self._gui_node

    @property
    def is_connected(self):
        return self._connected


    def connect(self):

        if self._connected:
            return

        self._executor = MultiThreadedExecutor()

        self._gui_node = Turtlebot3PyQtGuiNode()

        self._nodes = [
            self._gui_node
        ]

        for node in self._nodes:
            self._executor.add_node(node)

        self._connected = True

        SignalsManager.emit_ros_node_connection_changed(self._connected)


    def disconnect(self):

        if not self._connected:
            return

        for node in self._nodes:
            node.destroy_node()

        self._executor.shutdown()

        self._executor = None
        self._gui_node = None
        self._nodes.clear()
        self._connected = False

        SignalsManager.emit_ros_node_connection_changed(self._connected)


    def spin_once(self):

        if not self._connected:
            return

        self._executor.spin_once(timeout_sec=0)

