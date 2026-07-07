from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QLabel


class CmdVelWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        cmd_group = QGroupBox("Velocity Control (/cmd_vel)")
        cmd_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        cmd_layout = QFormLayout()

        self.linear_input = QLineEdit("0.10")
        self.angular_input = QLineEdit("0.50")
        cmd_layout.addRow("Linear m/s", self.linear_input)
        cmd_layout.addRow("Angular rad/s", self.angular_input)

        cmd_group.setLayout(cmd_layout)
        layout.addWidget(cmd_group)

        button_layout = QHBoxLayout()
        self.btn_left = QPushButton("Left")
        self.btn_stop = QPushButton("STOP")
        self.btn_right = QPushButton("Right")
        button_layout.addWidget(self.btn_left)
        button_layout.addWidget(self.btn_stop)
        button_layout.addWidget(self.btn_right)
        layout.addLayout(button_layout)

        button_layout2 = QHBoxLayout()
        self.btn_forward = QPushButton("Forward")
        self.btn_backward = QPushButton("Backward")
        button_layout2.addWidget(self.btn_forward)
        button_layout2.addWidget(self.btn_backward)
        layout.addLayout(button_layout2)

        self.status_label = QLabel("Command status")
        layout.addWidget(self.status_label)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_left.clicked.connect(self.viewmodel.left)
        self.btn_stop.clicked.connect(self.viewmodel.stop)
        self.btn_right.clicked.connect(self.viewmodel.right)
        self.btn_forward.clicked.connect(self.viewmodel.forward)
        self.btn_backward.clicked.connect(self.viewmodel.backward)
        self.linear_input.editingFinished.connect(self._update_velocity)
        self.angular_input.editingFinished.connect(self._update_velocity)
        self.viewmodel.status_changed.connect(self._on_status_changed)
        self.viewmodel.velocity_changed.connect(self._on_velocity_changed)

    def _update_velocity(self):
        if self.viewmodel is None:
            return
        try:
            linear = float(self.linear_input.text())
            angular = float(self.angular_input.text())
            self.viewmodel.set_velocity(linear, angular)
        except ValueError:
            pass

    def _on_status_changed(self, message):
        self._update_status_text(message)

    def _on_velocity_changed(self, linear, angular):
        self._update_status_text(f"linear={linear:.2f}, angular={angular:.2f}")

    def _update_status_text(self, message):
        if self.viewmodel is None:
            return
        self.status_label.setText(
            f"{message}\n"
            f"current linear={self.viewmodel.linear:.2f}, angular={self.viewmodel.angular:.2f}"
        )
