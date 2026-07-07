from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class ProcessControlViewModel(QObject):
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, launch_service):
        super().__init__()
        self.launch_service = launch_service

    @pyqtSlot()
    def run_bringup(self):
        self._execute(self.launch_service.run_bringup, "Bringup started")

    @pyqtSlot()
    def run_slam(self):
        self._execute(self.launch_service.run_slam, "SLAM started")

    @pyqtSlot()
    def run_nav2(self):
        self._execute(self.launch_service.run_nav2, "Nav2 started")

    @pyqtSlot()
    def run_rviz2(self):
        self._execute(self.launch_service.run_rviz2, "Rviz2 started")

    @pyqtSlot()
    def save_map(self):
        self._execute(self.launch_service.save_map, "Map save requested")

    @pyqtSlot()
    def stop_launches(self):
        self._execute(self.launch_service.stop_launches, "Stop launches requested")

    def _execute(self, action, success_message):
        try:
            action()
            self.status_changed.emit(success_message)
        except Exception as exc:
            self.error_occurred.emit(str(exc))
