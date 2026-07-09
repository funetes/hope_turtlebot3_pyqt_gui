import math

from sympy import im

from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import BatteryState, LaserScan
from tf_transformations import euler_from_quaternion
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler

from ..models.waypoint import Waypoint
from ..models.trajectory import Trajectory
from ..models.robot_topic_info import RobotTopicInfo
from ..signals.RosSignalsManager import SignalsManager

class Turtlebot3PyQtGuiNode(Node):
    def __init__(self):
        super().__init__("turtlebot3_pyqt_gui")
        # self._timer = self.create_timer(0.01, self._spin_once)

        self.signalsManager = SignalsManager

        self.robot_topic_info = RobotTopicInfo()

        self._robot_topic_timer = self.create_timer(0.5, self._robot_topic_emit)

        # traject 주행 client
        self.set_follow_waypoints_client()
        # 지정된 하나의 경유점 까지 주행
        self.set_action_client()

        self.set_subscription()

    def set_follow_waypoints_client(self):
        # FollowWaypoints Action Client 생성
        self._follow_waypoints_client = ActionClient(
            self,
            FollowWaypoints,
            "follow_waypoints",
        )

    def set_action_client(self):
        self._navigate_client = ActionClient(self, NavigateToPose, "navigate_to_pose")

    def set_subscription(self):

        self.battery_sub = self.create_subscription(
            BatteryState, "/battery_state", self._battery_state_callback, 10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            "/odom",
            self._odom_callback,
            10,
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            "/scan",
            self._scan_callback,
            qos_profile_sensor_data,
        )

    def _odom_callback(self, msg: Odometry):

        self.robot_topic_info.pos_x = msg.pose.pose.position.x
        self.robot_topic_info.pos_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, self.robot_topic_info.yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

    def _scan_callback(self, msg: LaserScan):
        valid = [r for r in msg.ranges if not math.isinf(r) and not math.isnan(r)]

        # print(len(valid))

        self.robot_topic_info.min_distance = min(valid) if valid else float("inf")

    def _battery_state_callback(self, msg: BatteryState):
        self.signalsManager.battery_status_received.emit(msg)

    def _robot_topic_emit(self):

        # self.get_logger().info("_robot_topic_emit")
        # print(self.robot_topic_info)
        self.signalsManager.robot_topic_info_received.emit(self.robot_topic_info)

    def navigate_to_waypoint(self, waypoint: Waypoint) -> bool:

        if not self._navigate_client.wait_for_server(timeout_sec=3.0):
            self.get_logger().warning(
                "Navigation server is unavailable."
            )
            return False

        goal = NavigateToPose.Goal()


        self._navigate_client.send_goal_async(goal)

        return True

    # def _spin_once(self):
    #     rclpy.spin_once(self, timeout_sec=0)

    def follow_trajectory(self, trajectory: Trajectory):

        """
        Trajectory를 FollowWaypoints Action으로 전송한다.
        """
        self.get_logger().info("follow_trajectory()")
        # Nav2 서버가 준비될 때까지 대기
        if not self._follow_waypoints_client.wait_for_server(timeout_sec=3.0):
            self.get_logger().warning(
                "navi server is not open yet"
            )
            return

        # Action Goal 생성
        goal = FollowWaypoints.Goal()

        # Goal에 Pose 목록 저장
        goal.poses = [
            waypoint.to_pose_stamped(self.get_clock()) for waypoint in trajectory.waypoints
        ]

        # Action 전송
        future = self._follow_waypoints_client.send_goal_async(goal)

        # Goal 수락 여부 확인
        future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn("FollowWaypoints Goal Rejected")
            return

        self.get_logger().info("FollowWaypoints Started")

        result_future = goal_handle.get_result_async()

        result_future.add_done_callback(
            self._result_callback
        )

    def _result_callback(self, future):

        result = future.result().result

        self.get_logger().info(
            "Trajectory Finished"
        )

        self.get_logger().info(
            f"Missed Waypoints : {result.missed_waypoints}"
        )
