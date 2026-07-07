from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class WaypointViewModel(QObject):
    waypoint_added = pyqtSignal(str)
    waypoint_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_waypoint = ""

    @pyqtSlot(float, float, float)
    def add_waypoint(self, x, y, yaw):
        self.current_waypoint = f"X:{x:.2f}, Y:{y:.2f}, Yaw:{yaw:.2f}"
        self.waypoint_added.emit(self.current_waypoint)

    @pyqtSlot()
    def go_to_waypoint(self):
        if not self.current_waypoint:
            self.waypoint_requested.emit("No waypoint set")
            return
        self.waypoint_requested.emit(f"Moving to {self.current_waypoint}")
