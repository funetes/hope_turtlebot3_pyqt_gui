from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ..services.waypoints_yaml_load_service import WaypointYamlLoadService
from ..models.waypoint import Waypoint

class WaypointViewModel(QObject):

    waypoints_loaded = pyqtSignal(list)
    waypoint_selected = pyqtSignal(Waypoint)
    waypoint_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._yaml_service = WaypointYamlLoadService()
        self._waypoints: list[Waypoint] = []

        self._selected_waypoint: Waypoint | None  = None

    @property
    def selected_waypoint(self):
        return self._selected_waypoint

    def load_waypoints(self, path):

        self._waypoints = self._yaml_service.load(path)

        print(self._waypoints)

        self.waypoints_loaded.emit(
            [wp.name for wp in self._waypoints]
        )

        if self._waypoints:
            self.select_waypoint(0)


    # @pyqtSlot(float, float, float)
    # def add_waypoint(self, x, y, yaw):
        # self.current_waypoint = f"X:{x:.2f}, Y:{y:.2f}, Yaw:{yaw:.2f}"
        # self.waypoint_added.emit(self.current_waypoint)

    @pyqtSlot()
    def go_to_waypoint(self):
        pass


    @pyqtSlot(int)
    def select_waypoint(self, index: int):

        if index < 0:
            return

        if index >= len(self._waypoints):
            return

        self._selected_waypoint = self._waypoints[index]

        self.waypoint_selected.emit(self._selected_waypoint)
