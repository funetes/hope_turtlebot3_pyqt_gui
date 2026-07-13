from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class ProcessControlViewModel(QObject):
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, launch_service):
        super().__init__()
        self.launch_service = launch_service
        self.launch_service.set_viewmodel(self);

    @pyqtSlot()
    def run_bringup(self):
        self._execute(self.launch_service.run_bringup, "Bringup requested")
    
    @pyqtSlot()
    def stop_bringup(self):
        self._execute(self.launch_service.stop_bringup, "Bringup Stop requested")

    @pyqtSlot()
    def run_slam(self):
        self._execute(self.launch_service.run_slam, "SLAM requested")

    @pyqtSlot()
    def run_nav2(self):
        self._execute(self.launch_service.run_nav2, "Nav2 requested")

    @pyqtSlot()
    def run_rviz2(self):
        self._execute(self.launch_service.run_rviz2, "Rviz2 requested")

    @pyqtSlot()
    def save_map(self):
        self._execute(self.launch_service.save_map, "Map saveed")

    @pyqtSlot()
    def stop_launches(self):
        self._execute(self.launch_service.stop_launches, "Stop launches requested")

    @pyqtSlot()
    def start_camera(self):
        self._execute(self.launch_service.start_camera, "camera node start requested")

    @pyqtSlot()
    def stop_camera(self):
        self._execute(self.launch_service.stop_camera, "camera node stop requested")

    def _execute(self, action, success_message):
        try:
            action()
            self.status_changed.emit(success_message)
        except Exception as exc:
            self.error_occurred.emit(str(exc))
