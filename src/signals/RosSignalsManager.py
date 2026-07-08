from PyQt5.QtCore import QObject, pyqtSignal

from sensor_msgs.msg import BatteryState

class ROSSignalsManager(QObject):

    # 필요한 시그널 정의
    service_response_received = pyqtSignal(dict)
    node_status_changed = pyqtSignal(str)
    battery_status_received = pyqtSignal(BatteryState)
    robot_topic_info_received = pyqtSignal(object)

    def __init__(self):
      super().__init__()

    def emit_service_response(self, data: dict):
        self.service_response_received.emit(data)

    def emit_status(self, status: str):
        self.node_status_changed.emit(status)

    def emit_battery_status(self, status: BatteryState):
        self.battery_status_received.emit(status)


    def emit_robot_topic_info(self, robot_topic_info):
        self.robot_topic_info_received.emit(robot_topic_info)


# 파일의 맨 아래에서 인스턴스를 미리 '하나만' 생성해 둡니다.
SignalsManager = ROSSignalsManager()
