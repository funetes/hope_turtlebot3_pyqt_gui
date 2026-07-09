import subprocess
from typing import List
from pathlib import Path
import yaml

from ..models.trajectory import Trajectory
from ..models.waypoint import Waypoint

class TrajectoryService:
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
        # 실제 실행이 필요하면 별도 프로세스/스레드로 실행
        subprocess.Popen(["echo", f"Running {trajectory}"])
