
from pathlib import Path
from typing import List
import yaml

from ..models.waypoint import Waypoint


class WaypointYamlLoadService:

    def load(self, file_path: str | Path) -> List[Waypoint]:

        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        waypoints = [
            Waypoint.from_dict(item) for item in data["waypoints"]
        ]

        return waypoints
