from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from signals.RosSignalsManager import SignalsManager
from turtlebot3_pyqt_gui.ros.turtlebot3_pyqt_gui_node import RobotTopicInfo

class Ros2TopicViewModel(QObject):
    topics_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.topics = "/cmd_vel\n/odom\n/tf\n/scan"

        # 싱글턴 인스턴스 획득
        self.signal_manager = SignalsManager

        self.signal_manager.robot_topic_info_received.connect(self.refresh_topics)

    @pyqtSlot(str, RobotTopicInfo)
    def refresh_topics(self, robot_topic_info: RobotTopicInfo):
        topic_text = (
            f"현재 위치 x : {robot_topic_info.pos_x}"
            f"현재 위치 y : {robot_topic_info.pos_y}"
            f"현재 방향 yaw : {robot_topic_info.yaw}"
            f"LiDAR 최소 거리 : {robot_topic_info.min_distance} m"
        )
        print(topic_text)
        self.topics_changed.emit(topic_text)
