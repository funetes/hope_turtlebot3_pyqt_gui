from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ..models.trajectory import Trajectory


class TrajectoryViewModel(QObject):
    trajectories_loaded = pyqtSignal(list)
    trajectory_selected = pyqtSignal(str)
    trajectory_started = pyqtSignal(str)

    def __init__(self, trajectory_service):
        super().__init__()
        self._yaml_service = trajectory_service
        self.trajectory_service = trajectory_service
        self._selected_trajectory: Trajectory | None = None

    @pyqtSlot(str)
    def load_trajectory(self, trajectory):
        self.trajectory_service.load_trajectory(trajectory)
        self.trajectory_loaded.emit(trajectory)

    @pyqtSlot(str)
    def run_trajectory(self, trajectory):
        self.trajectory_service.run_trajectory(trajectory)
        self.trajectory_started.emit(trajectory)


    def load_trajectories(self, path):

        self._trajectories = self._yaml_service.load(path)

        # print(self._trajectories)
        names = [tr.name for tr in self._trajectories]
        # print(names)
        self.trajectories_loaded.emit(names)

        if self._trajectories:
            self.select_trajectory(0)


    @pyqtSlot(int)
    def select_trajectory(self, index: int):

        if index < 0:
            return

        if index >= len(self._trajectories):
            return

        self._selected_trajectory = self._trajectories[index]
        count = len(self._selected_trajectory.waypoints)
        print(f"waypoints count{count}")
        self.trajectory_selected.emit(self._selected_trajectory.name)
