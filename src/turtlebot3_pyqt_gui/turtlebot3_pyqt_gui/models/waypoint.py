# entity/waypoint.py

from dataclasses import dataclass


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

#  - name: point1

#     frame_id: map

#     pose:

#       position:

#         x: 32.5246347706

#         y: -9.05557767837

#         z: 0.0

#       angle:

#         yaw: 89.9111495477
