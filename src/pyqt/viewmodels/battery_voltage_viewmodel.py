from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class BatteryVoltageViewModel(QObject):
    status_changed = pyqtSignal(str, str, int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str, int)
    def update_status(self, voltage, capacity, percentage):
        self.status_changed.emit(voltage, capacity, percentage)
