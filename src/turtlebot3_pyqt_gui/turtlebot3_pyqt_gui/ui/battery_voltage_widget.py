from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGroupBox, QFormLayout, QLineEdit


class BatteryVoltageWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None
        layout = QVBoxLayout(self)

        battery_group = QGroupBox("Battery / Voltage")
        battery_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        battery_layout = QFormLayout()

        self.voltage_field = QLineEdit("12.8 V")
        self.voltage_field.setReadOnly(True)
        self.capacity_field = QLineEdit("95 %")
        self.capacity_field.setReadOnly(True)

        battery_layout.addRow("Voltage", self.voltage_field)
        battery_layout.addRow("Capacity", self.capacity_field)

        battery_group.setLayout(battery_layout)
        layout.addWidget(battery_group)

        self.progress = QProgressBar()
        self.progress.setValue(95)
        layout.addWidget(self.progress)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.viewmodel.status_changed.connect(self.update_status)

    def update_status(self, voltage, percentage):
        self.voltage_field.setText(voltage)
        self.capacity_field.setText(f"{percentage} %")
        self.progress.setValue(int(percentage))
