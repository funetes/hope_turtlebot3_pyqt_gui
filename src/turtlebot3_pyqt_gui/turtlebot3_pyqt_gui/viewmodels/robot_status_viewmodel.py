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
        self._emit_status()

    @pyqtSlot()
    def disconnect(self):
        self.ros_state = "Disconnected"
        self._emit_status()

    @pyqtSlot()
    def exit(self):
        self._emit_status("Application exit requested")

    @pyqtSlot(float, float)
    def update_cmd_vel(self, linear, angular):
        self.last_cmd = f"linear: {linear:.2f}, angular: {angular:.2f}"
        self._emit_status()

    def _emit_status(self, message=None):
        if message is None:
            message = self.last_cmd
        self.status_changed.emit(self.ros_state, self.min_scan, message)
