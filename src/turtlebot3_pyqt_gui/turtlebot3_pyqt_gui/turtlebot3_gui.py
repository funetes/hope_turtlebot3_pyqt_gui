import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import rclpy
from rclpy.node import Node

from .ros.turtlebot3_pyqt_gui_node import Turtlebot3PyQtGuiNode

PYQT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pyqt'))
if PYQT_ROOT not in sys.path:
    sys.path.insert(0, PYQT_ROOT)

from turtlebot3_pyqt_gui.turtlebot3_pyqt import MainWindow




def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)
    gui_node = Turtlebot3PyQtGuiNode()
    main = MainWindow(gui_node)
    main.show()

    qt_timer = QTimer()
    qt_timer.timeout.connect(lambda: rclpy.spin_once(gui_node, timeout_sec=0))
    qt_timer.start(10)

    exit_code = app.exec_()
    gui_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
