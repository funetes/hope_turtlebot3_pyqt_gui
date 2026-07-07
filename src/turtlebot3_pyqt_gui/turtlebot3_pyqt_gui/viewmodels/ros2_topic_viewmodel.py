from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Ros2TopicViewModel(QObject):
    topics_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.topics = "/cmd_vel\n/odom\n/tf\n/scan"

    @pyqtSlot()
    def refresh_topics(self):
        self.topics_changed.emit(self.topics)
