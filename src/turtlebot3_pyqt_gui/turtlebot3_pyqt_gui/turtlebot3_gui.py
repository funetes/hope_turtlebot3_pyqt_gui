import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import rclpy
from rclpy.node import Node

from .ros.turtlebot3_pyqt_gui_node import Turtlebot3PyQtGuiNode
from .ros.robot_connection import RobotConnection

PYQT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pyqt'))
if PYQT_ROOT not in sys.path:
    sys.path.insert(0, PYQT_ROOT)

from turtlebot3_pyqt_gui.turtlebot3_pyqt import MainWindow




def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)


    connection = RobotConnection()
    connection.node_connect()

    window = MainWindow(connection.node)
    window.show()

    timer = QTimer()
    timer.timeout.connect(connection.spin_once)
    timer.start(10)

    exit_code = app.exec_()

    connection.node_disconnect()

    rclpy.shutdown()

    sys.exit(exit_code)



if __name__ == '__main__':
    main()
