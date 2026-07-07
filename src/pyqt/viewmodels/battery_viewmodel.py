from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class BatteryViewModel(QObject):
    status_changed = pyqtSignal(float, int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(float, int)
    def update_status(self, voltage, percentage):
        self.status_changed.emit(voltage, percentage)
