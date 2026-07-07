from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QComboBox, QLabel


class TrajectoryWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        traj_group = QGroupBox("Trajectory Selection")
        traj_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        traj_layout = QVBoxLayout()

        self.trajectory_combo = QComboBox()
        self.trajectory_combo.addItems(["Trajectory A", "Trajectory B", "Trajectory C"])
        traj_layout.addWidget(self.trajectory_combo)
        traj_group.setLayout(traj_layout)

        layout.addWidget(traj_group)

        run_row = QHBoxLayout()
        self.btn_load = QPushButton("Load")
        self.btn_run = QPushButton("Run")
        run_row.addWidget(self.btn_load)
        run_row.addWidget(self.btn_run)
        layout.addLayout(run_row)

        self.status_label = QLabel("Trajectory status")
        layout.addWidget(self.status_label)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_load.clicked.connect(self._on_load)
        self.btn_run.clicked.connect(self._on_run)
        self.viewmodel.trajectory_loaded.connect(self._on_trajectory_loaded)
        self.viewmodel.trajectory_started.connect(self._on_trajectory_started)

    def _on_load(self):
        if self.viewmodel is None:
            return
        self.viewmodel.load_trajectory(self.trajectory_combo.currentText())

    def _on_run(self):
        if self.viewmodel is None:
            return
        self.viewmodel.run_trajectory(self.trajectory_combo.currentText())

    def _on_trajectory_loaded(self, trajectory):
        self.status_label.setText(f"Loaded {trajectory}")

    def _on_trajectory_started(self, trajectory):
        self.status_label.setText(f"Running {trajectory}")
