from PyQt5.QtCore import QObject, pyqtSignal


class LogViewModel(QObject):
    log_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def append_log(self, message):
        self.log_updated.emit(message)
