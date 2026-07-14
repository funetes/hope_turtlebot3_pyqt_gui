from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ..signals.RosSignalsManager import SignalsManager


class Ros2TopicViewModel(QObject):
    topics_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.topics = "/cmd_vel\n/odom\n/tf\n/scan"

        # 싱글턴 인스턴스 획득
        self.signal_manager = SignalsManager

        self.signal_manager.robot_topic_info_received.connect(
            self.update_robot_topic_info
        )

    def update_robot_topic_info(self, robot_topic_info):
        topic_text = (
            f"현재 위치 x : {robot_topic_info.pos_x:.3f}\n"
            f"현재 위치 y : {robot_topic_info.pos_y:.3f}\n"
            f"현재 방향 yaw : {robot_topic_info.yaw:.3f}\n"
            f"LiDAR 최소 거리 : {robot_topic_info.min_distance:.2f} m"
        )
        self.topics_changed.emit(topic_text)

    @pyqtSlot()
    def refresh_topics(self):
        pass
