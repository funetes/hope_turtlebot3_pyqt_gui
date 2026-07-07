from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, QHBoxLayout


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
        self.min_scan = QLineEdit("0.25 m")
        self.min_scan.setReadOnly(True)
        self.last_cmd = QLineEdit("linear: 0.00, angular: 0.00")
        self.last_cmd.setReadOnly(True)

        status_layout.addRow("ROS", self.ros_state)
        status_layout.addRow("Min Scan (m)", self.min_scan)
        status_layout.addRow("Last cmd vel", self.last_cmd)

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
        self.btn_exit.clicked.connect(self.viewmodel.exit)
        self.viewmodel.status_changed.connect(self.update_status)

    def update_status(self, ros_state, min_scan, last_cmd):
        self.ros_state.setText(ros_state)
        self.min_scan.setText(min_scan)
        self.last_cmd.setText(last_cmd)
