from dataclasses import dataclass

@dataclass(slots=True)
class RobotTopicInfo:
    pos_x: float = 0.0
    pos_y: float = 0.0
    yaw: float = 0.0
    min_distance: float = float("inf")
