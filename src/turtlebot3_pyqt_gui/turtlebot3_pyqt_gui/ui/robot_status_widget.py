from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QApplication


class RobotStatusWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        status_group = QGroupBox("Robot Status")
        status_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        status_layout = QFormLayout()

        self.ros_state = QLineEdit("Connected")
        self.ros_state.setReadOnly(True)

        status_layout.addRow("ROS", self.ros_state)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        button_row = QHBoxLayout()
        self.btn_connect = QPushButton("Connect")
        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_exit = QPushButton("Exit")
        button_row.addWidget(self.btn_connect)
        button_row.addWidget(self.btn_disconnect)
        button_row.addWidget(self.btn_exit)
        layout.addLayout(button_row)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)


    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_connect.clicked.connect(self.viewmodel.connect)
        self.btn_disconnect.clicked.connect(self.viewmodel.disconnect)
        self.btn_exit.clicked.connect(QApplication.quit)

        self.viewmodel.status_changed.connect(self.update_status)

    def update_status(self, ros_state):
        self.ros_state.setText(ros_state)
