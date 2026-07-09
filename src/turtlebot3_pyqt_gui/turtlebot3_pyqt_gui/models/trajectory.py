# entity/waypoint.py

from dataclasses import dataclass
from .waypoint import Waypoint
from typing import List

@dataclass(slots=True)
class Trajectory:
    name: str
    waypoints: List[Waypoint]

    @classmethod
    def from_dict(cls, data: dict, waypoints: List[Waypoint]) -> "Trajectory":

        selected = []

        for waypoint_name in data["waypoints"]:
            waypoint = next(
                wp for wp in waypoints if wp.name == waypoint_name
            )
            selected.append(waypoint)

        return cls(
                    name=data["name"],
                    waypoints= selected,
                )

# trajectories:
#   - name: Traj1
#     waypoints:
#     - point2
#     - point3
#     - point5
#     - point6
#     - point7
#     - point8
#     - point9
#     - point10
#     - point11
#     - point12
#     - point5
#     - point3
#     - point2
