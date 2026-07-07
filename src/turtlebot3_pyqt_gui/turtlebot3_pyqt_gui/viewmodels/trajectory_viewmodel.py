from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TrajectoryViewModel(QObject):
    trajectory_loaded = pyqtSignal(str)
    trajectory_started = pyqtSignal(str)

    def __init__(self, trajectory_service):
        super().__init__()
        self.trajectory_service = trajectory_service

    @pyqtSlot(str)
    def load_trajectory(self, trajectory):
        self.trajectory_service.load_trajectory(trajectory)
        self.trajectory_loaded.emit(trajectory)

    @pyqtSlot(str)
    def run_trajectory(self, trajectory):
        self.trajectory_service.run_trajectory(trajectory)
        self.trajectory_started.emit(trajectory)
