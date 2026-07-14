
from pathlib import Path
from typing import List
import yaml

from ..ros.ros_manager import IROSManager

from ..models.waypoint import Waypoint


class WaypointService:

    def __init__(self, ros: IROSManager):
        self._ros = ros

    def load(self, file_path: str | Path) -> List[Waypoint]:

        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        waypoints = [
            Waypoint.from_dict(item) for item in data["waypoints"]
        ]

        return waypoints

    def run_to_waypoint(self, waypoint):
        if waypoint is None:
            print("선택된 경유점이 없습니다.")

        success = self._ros.gui_node.navigate_to_waypoint(waypoint)

        if success:
            print("Navigation started.")
        else:
            print("Navigation server unavailable.")
