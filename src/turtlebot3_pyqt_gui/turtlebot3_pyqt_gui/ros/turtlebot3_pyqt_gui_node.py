import math

from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import BatteryState, LaserScan
from tf_transformations import euler_from_quaternion

from ..models.robot_topic_info import RobotTopicInfo
from ..signals.RosSignalsManager import SignalsManager


class Turtlebot3PyQtGuiNode(Node):
    def __init__(self):
        super().__init__("turtlebot3_pyqt_gui")
        # self._timer = self.create_timer(0.01, self._spin_once)

        self.signalsManager = SignalsManager

        self.robot_topic_info = RobotTopicInfo()

        self._robot_topic_timer = self.create_timer(0.5, self._robot_topic_emit)

        self.set_subscription()

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

    # def _spin_once(self):
    #     rclpy.spin_once(self, timeout_sec=0)
