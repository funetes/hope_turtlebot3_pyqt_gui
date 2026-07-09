from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from rclpy.node import Node
from robot_audio_interfaces.msg import AudioCommand

import requests

class TeamCustomViewModel(QObject):
    action_triggered = pyqtSignal(str)

    def __init__(self, ros_node: Node):
        super().__init__()
        self.ros_node = ros_node
        self.weather = None

    def get_env_status(self):
        try:
            # 1. 위치 좌표 가져오기
            geo_res = requests.get("http://ip-api.com/json/").json()
            city = geo_res.get("city", "Seoul")
            
            # 2. 해당 위치의 한 줄 날씨 가져오기
            weather_res = requests.get(f"http://wttr.in/{city}?format=1&lang=ko")
            weather_text = weather_res.text.strip()
            
            self.ros_node.get_logger().info(f"🤖 [터틀봇 상태] 현재 위치: {city} | 날씨: {weather_text}")
            
            msg = AudioCommand()
            msg.type = AudioCommand.TYPE_TTS
            msg.text = f"서울 현재 {weather_text}"
            msg.volume = 0.1
            msg.repeat = 1

            self.ros_node.audio_publisher.publish(msg)
            self.weather = msg.text
        except Exception as e:
            self.ros_node.get_logger().error(f"API 호출 실패: {e}")

    @pyqtSlot()
    def get_weather(self):
        self.get_env_status()
        if self.weather is not None:
            self.action_triggered.emit(self.weather)

