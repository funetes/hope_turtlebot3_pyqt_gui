import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class RobotStatusViewModel(QObject):
    status_changed = pyqtSignal(str, str, str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ros_state = "Disconnected"
        self.min_scan = "--"
        self.last_cmd = "--"

    @pyqtSlot()
    def connect(self):
        domain_id = '60'
        os.environ['ROS_DOMAIN_ID'] = domain_id if domain_id else '60'
        self.ros_state = f'domain_id: {domain_id} connected.'
        self.min_scan = ""
        self._emit_status()

    @pyqtSlot()
    def disconnect(self):
        self.ros_state = "Disconnected"
        self._emit_status()

    @pyqtSlot()
    def exit(self):
        self._emit_status("Application exit requested")

    def _emit_status(self, message=None):
        if message is None:
            message = self.last_cmd
        self.status_changed.emit(self.ros_state, self.min_scan, message)
