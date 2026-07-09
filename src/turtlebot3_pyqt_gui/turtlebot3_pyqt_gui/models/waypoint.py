# entity/waypoint.py

from dataclasses import dataclass
from turtle import pos

from geometry_msgs.msg import PoseStamped

from tf_transformations import quaternion_from_euler

@dataclass(slots=True)
class Waypoint:
    name: str
    frame_id: str
    x: float
    y: float
    yaw: float

    @classmethod
    def from_dict(cls, data: dict) -> "Waypoint":

        position = data["pose"]["position"]
        angle = data["pose"]["angle"]

        return cls(
            name=data["name"],
            frame_id=data.get("frame_id", "map"),
            x=float(position["x"]),
            y=float(position["y"]),
            yaw=float(angle["yaw"]),
        )

    def to_pose_stamped(self, clock) -> PoseStamped:
            # PoseStamped 생성
        pose = PoseStamped()

        # 기준 좌표계(map)
        pose.header.frame_id = self.frame_id

        # 현재 시간
        pose.header.stamp = clock.now().to_msg()

            # 위치 설정
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        pose.pose.position.z = 0.0

        # yaw → quaternion 변환
        q = quaternion_from_euler(
            0.0,
            0.0,
            self.yaw,
        )
        return pose

#  - name: point1

#     frame_id: map

#     pose:

#       position:

#         x: 32.5246347706

#         y: -9.05557767837

#         z: 0.0

#       angle:

#         yaw: 89.9111495477
