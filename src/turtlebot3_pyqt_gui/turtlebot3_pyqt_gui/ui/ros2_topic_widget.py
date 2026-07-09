from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit, QPushButton


class Ros2TopicWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        topic_group = QGroupBox("ROS 2 Topic Monitor")
        topic_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        topic_layout = QVBoxLayout()

        self.topic_text = QTextEdit()
        self.topic_text.setReadOnly(True)
        self.topic_text.setFixedHeight(180)
        self.btn_refresh = QPushButton("Refresh")

        topic_layout.addWidget(self.topic_text)
        topic_group.setLayout(topic_layout)
        layout.addWidget(topic_group)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_refresh.clicked.connect(self.viewmodel.refresh_topics)
        self.viewmodel.topics_changed.connect(self._on_topics_changed)
        self.viewmodel.refresh_topics()

    def _on_topics_changed(self, topics):
        self.topic_text.setPlainText(topics)
