import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ..signals.RosSignalsManager import SignalsManager
from ..ros.ros_manager import IROSManager

class RobotStatusViewModel(QObject):
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, ros: IROSManager):
        super().__init__()
        self._ros = ros
        self.ros_state = "Disconnected"

        SignalsManager.ros_node_connection_changed.connect(self._connection_changed)


    @pyqtSlot()
    def connect(self):
        domain_id = '60'
        os.environ['ROS_DOMAIN_ID'] = domain_id if domain_id else '60'
        # self.ros_state = f'domain_id: {domain_id} connected.'
        # self.min_scan = ""
        # self._emit_status()
        # SignalsManager.ros_connect_requested.emit()
        self._ros.connect()

    @pyqtSlot()
    def disconnect(self):
        # self.ros_state = "Disconnected"
        # self._emit_status()
        # SignalsManager.ros_disconnect_requested.emit()
        self._ros.disconnect()

    @pyqtSlot()
    def exit(self):
        self._emit_status("Application exit requested")

    @pyqtSlot(bool)
    def _connection_changed(self, isConnected):
        self._emit_status("connected" if isConnected else  "Disconnected")

    @pyqtSlot(bool)
    def _emit_status(self, message):
        self.status_changed.emit(message)
