from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QLabel


class ProcessControlWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None
        layout = QVBoxLayout(self)

        launch_group = QGroupBox("Launch Control")
        launch_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        launch_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        self.btn_run_bringup = QPushButton("Run Bringup")
        self.btn_run_slam = QPushButton("Run SLAM")
        self.btn_stop_bringup = QPushButton("Stop Bringup")
        row1.addWidget(self.btn_run_bringup)
        row1.addWidget(self.btn_stop_bringup)
        row1.addWidget(self.btn_run_slam)
        launch_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.btn_run_nav2 = QPushButton("Run Nav2")
        self.btn_run_rviz2 = QPushButton("Run Rviz2")
        row2.addWidget(self.btn_run_nav2)
        row2.addWidget(self.btn_run_rviz2)
        launch_layout.addLayout(row2)

        row3 = QHBoxLayout()
        self.btn_save_map = QPushButton("Save Map")
        self.btn_stop_launches = QPushButton("Stop Launches")
        row3.addWidget(self.btn_save_map)
        row3.addWidget(self.btn_stop_launches)
        launch_layout.addLayout(row3)

        launch_group.setLayout(launch_layout)
        layout.addWidget(launch_group)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_run_bringup.clicked.connect(self.viewmodel.run_bringup)
        self.btn_stop_bringup.clicked.connect(self.viewmodel.stop_bringup)
        self.btn_run_slam.clicked.connect(self.viewmodel.run_slam)
        self.btn_run_nav2.clicked.connect(self.viewmodel.run_nav2)
        self.btn_run_rviz2.clicked.connect(self.viewmodel.run_rviz2)
        self.btn_save_map.clicked.connect(self.viewmodel.save_map)
        self.btn_stop_launches.clicked.connect(self.viewmodel.stop_launches)

        self.viewmodel.status_changed.connect(self._on_status_changed)
        self.viewmodel.error_occurred.connect(self._on_error_occurred)

    def _on_status_changed(self, message):
        self.status_label.setText(message)

    def _on_error_occurred(self, message):
        self.status_label.setText(f"Error: {message}")
