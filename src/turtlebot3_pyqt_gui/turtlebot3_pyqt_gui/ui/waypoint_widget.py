from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel


class WaypointWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        waypoint_group = QGroupBox("Waypoint Registration")
        waypoint_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        waypoint_layout = QFormLayout()

        self.x_input = QLineEdit("0.00")
        self.y_input = QLineEdit("0.00")
        self.yaw_input = QLineEdit("0.00")
        waypoint_layout.addRow("X", self.x_input)
        waypoint_layout.addRow("Y", self.y_input)
        waypoint_layout.addRow("Yaw", self.yaw_input)

        waypoint_group.setLayout(waypoint_layout)
        layout.addWidget(waypoint_group)

        button_row = QHBoxLayout()
        self.btn_add_waypoint = QPushButton("Add Waypoint")
        self.btn_go_waypoint = QPushButton("Go To Waypoint")
        button_row.addWidget(self.btn_add_waypoint)
        button_row.addWidget(self.btn_go_waypoint)
        layout.addLayout(button_row)

        self.status_label = QLabel("Waypoint status")
        layout.addWidget(self.status_label)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_add_waypoint.clicked.connect(self._on_add_waypoint)
        self.btn_go_waypoint.clicked.connect(self.viewmodel.go_to_waypoint)
        self.viewmodel.waypoint_added.connect(self._on_waypoint_added)
        self.viewmodel.waypoint_requested.connect(self._on_waypoint_requested)

    def _on_add_waypoint(self):
        if self.viewmodel is None:
            return
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            yaw = float(self.yaw_input.text())
            self.viewmodel.add_waypoint(x, y, yaw)
        except ValueError:
            self.status_label.setText("Invalid waypoint values")

    def _on_waypoint_added(self, waypoint):
        self.status_label.setText(f"Waypoint set: {waypoint}")

    def _on_waypoint_requested(self, message):
        self.status_label.setText(message)
