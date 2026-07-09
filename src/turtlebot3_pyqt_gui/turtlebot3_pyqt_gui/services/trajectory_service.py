
from typing import List
from pathlib import Path
import yaml

from ..models.trajectory import Trajectory
from ..models.waypoint import Waypoint

class TrajectoryService:

    def __init__(self, ros_node=None) -> None:
        self.ros_node = ros_node

    def load_trajectory(self, trajectory):
        # trajectory load 처리 예시
        return trajectory

    def load(self, file_path: str | Path) -> List[Trajectory]:

        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        waypoints = [Waypoint.from_dict(item) for item in data["waypoints"]]

        return [
            Trajectory.from_dict(traj, waypoints) for traj in data["trajectories"]
        ]

    def run_trajectory(self, trajectory):
        self.ros_node.follow_trajectory(trajectory)

