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
        self.ros_state = "Connected"
        self.min_scan = "0.25 m"
        self.last_cmd = "linear: 0.00, angular: 0.00"
        self.status_changed.emit(self.ros_state, self.min_scan, self.last_cmd)

    @pyqtSlot()
    def disconnect(self):
        self.ros_state = "Disconnected"
        self.status_changed.emit(self.ros_state, self.min_scan, self.last_cmd)

    @pyqtSlot()
    def exit(self):
        self.status_changed.emit(self.ros_state, self.min_scan, "Application exit requested")
