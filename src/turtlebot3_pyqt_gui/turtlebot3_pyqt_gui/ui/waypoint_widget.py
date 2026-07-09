from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WaypointWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()

        self.viewmodel = viewmodel

        layout = QVBoxLayout(self)

        waypoint_group = QGroupBox("Waypoint")
        waypoint_group.setStyleSheet("QGroupBox { font-weight: bold; }")

        group_layout = QVBoxLayout()

        form = QFormLayout()

        self.combo_waypoints = QComboBox()
        form.addRow("Waypoint", self.combo_waypoints)

        group_layout.addLayout(form)

        self.waypoint_info = QLabel("No waypoint selected")
        self.waypoint_info.setMinimumHeight(90)
        # self.waypoint_info.setStyleSheet("""
        #     QLabel {
        #         border: 1px solid gray;
        #         border-radius: 4px;
        #         padding: 8px;
        #         font-size: 15px;
        #         background: white;
        #     }
        # """)

        group_layout.addWidget(self.waypoint_info)

        waypoint_group.setLayout(group_layout)
        layout.addWidget(waypoint_group)

        # ------------------------------
        # Buttons
        # ------------------------------
        button_row = QHBoxLayout()

        self.btn_load_yaml = QPushButton("Load YAML")
        self.btn_go_waypoint = QPushButton("Go To Waypoint")

        button_row.addWidget(self.btn_load_yaml)
        button_row.addWidget(self.btn_go_waypoint)

        layout.addLayout(button_row)

        # ------------------------------
        # Status
        # ------------------------------
        self.status_label = QLabel("Waypoint status")
        layout.addWidget(self.status_label)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel

        self.btn_load_yaml.clicked.connect(self._on_load_yaml)
        self.btn_go_waypoint.clicked.connect(self.viewmodel.go_to_waypoint)

        self.combo_waypoints.currentIndexChanged.connect(self.viewmodel.select_waypoint)

        # ViewModel Signals
        self.viewmodel.waypoints_loaded.connect(self._on_waypoints_loaded)
        self.viewmodel.waypoint_selected.connect(self._on_waypoint_selected)
        self.viewmodel.waypoint_requested.connect(self.status_label.setText)

    def _on_load_yaml(self):

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Waypoint YAML", "", "YAML Files (*.yaml *.yml)"
        )

        if filename:
            # print(filename)
            self.viewmodel.load_waypoints(filename)
            self._on_waypoint_selected(self.viewmodel.selected_waypoint)

    def _on_waypoints_loaded(self, names):

        self.combo_waypoints.clear()
        self.combo_waypoints.addItems(names)

    def _on_waypoint_selected(self, waypoint):
        text = (
            f"X   : {waypoint.x:.3f}\nY   : {waypoint.y:.3f}\nYaw : {waypoint.yaw:.1f}°"
        )
        # print(text)
        self.waypoint_info.setText(text)
