import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import rclpy
from rclpy.node import Node

from .ros.ros_manager import IROSManager, ROSManager

PYQT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pyqt'))
if PYQT_ROOT not in sys.path:
    sys.path.insert(0, PYQT_ROOT)

from turtlebot3_pyqt_gui.turtlebot3_pyqt import MainWindow




def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)

    ros_manager: IROSManager = ROSManager()

    window = MainWindow(ros_manager)
    window.show()

    timer = QTimer()
    timer.timeout.connect(ros_manager.spin_once)
    timer.start(10)

    exit_code = app.exec_()

    ros_manager.disconnect()

    rclpy.shutdown()

    sys.exit(exit_code)



if __name__ == '__main__':
    main()
