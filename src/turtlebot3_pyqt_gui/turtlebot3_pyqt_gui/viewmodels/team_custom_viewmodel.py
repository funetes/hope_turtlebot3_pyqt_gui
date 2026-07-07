from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TeamCustomViewModel(QObject):
    action_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def custom_1(self):
        self.action_triggered.emit("Custom 1 executed")

    @pyqtSlot()
    def custom_2(self):
        self.action_triggered.emit("Custom 2 executed")
